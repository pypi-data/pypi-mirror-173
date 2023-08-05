import datetime
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

from timetable_cli.category import ActivityCategory
from timetable_cli.enums import ActivityTimeStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class ActivityStatus:
    title: str
    description: str = ""


@dataclass(kw_only=True)
class Activity:
    start: datetime.datetime
    title: str
    variation: str = ""
    category: Optional[ActivityCategory] = None
    colorscheme: dict = field(default_factory=dict)
    _timetable: Optional[Any] = None
    _activity_id: Optional[int] = None

    def activity_id(self, app) -> int:
        if self._activity_id:
            return self._activity_id
        result = self._get_activity_id(app)
        if not result:
            self._add_activity_to_db(app)
            result = self._get_activity_id(app)
        if result is None:
            raise TypeError
        self._activity_id = result
        return result

    def _get_activity_id(self, app) -> Optional[int]:
        sql = """SELECT id FROM activities WHERE \
title=? AND variation=? \
AND start=?;"""
        cur = app.connection.cursor()
        cur.execute(sql, [self.title, self.variation,
                          self.start.time().isoformat()])
        result = cur.fetchone()
        logger.debug(result)
        if result:
            return result[0]
        return None

    def _add_activity_to_db(self, app):
        sql = """INSERT INTO activities (title, variation, start) VALUES \
(?, ?, ?);"""
        con = app.connection
        cur = con.cursor()
        cur.execute(sql, [self.title, self.variation,
                          self.start.time().isoformat()])
        con.commit()

    def get_status(self, app: Any) -> ActivityStatus:
        """The status property."""
        sql = """SELECT status FROM records WHERE activity=? AND date=?;"""
        cur = app.connection.cursor()
        cur.execute(sql, [self.activity_id(app),
                          self.start.date().isoformat()])
        result = cur.fetchone()
        logger.debug(result)
        if result:
            return app.activity_status_variations[result[0]]
        result = app.activity_status_variations[0]
        self._set_status(app, result)
        return result

    def set_status(self, app: Any, value: ActivityStatus):
        self.get_status(app)
        self._update_status(app, value)

    def _set_status(self, app: Any, value: ActivityStatus):
        logger.debug(value)
        sql = """INSERT INTO records (activity, date, status) \
VALUES (?, ?, ?);"""
        app.connection.cursor().execute(
                sql, [self.activity_id(app),
                      self.start.date().isoformat(),
                      app.activity_status_variations.index(value)]
            )
        app.connection.commit()

    def _update_status(self, app: Any, value: ActivityStatus):
        logger.debug(value)
        sql = """UPDATE records SET status = ? WHERE \
activity = ? AND date = ?;"""
        app.connection.cursor().execute(
                sql, [app.activity_status_variations.index(value),
                      self.activity_id(app),
                      self.start.date().isoformat()]
            )
        app.connection.commit()

    def next(self):
        if not self._timetable:
            raise ValueError
        index = self._timetable.activities.index(self)
        if index == len(self._timetable.activities) - 1:
            return self._timetable.activities[0]
        return self._timetable.activities[index + 1]

    def total_time(self) -> datetime.timedelta:
        result = self.next().start - self.start
        if result.days < 0:
            result = datetime.timedelta(seconds=result.seconds)
        return result

    def eta(self, app) -> datetime.timedelta:
        return self.start - app.now()

    def time_status(self, datetime_input: datetime.datetime) -> ActivityTimeStatus:
        if datetime_input > self.start:
            if datetime_input > self.next().start:
                result = ActivityTimeStatus.BEFORE
            else:
                result = ActivityTimeStatus.NOW
        else:
            result = ActivityTimeStatus.AFTER
        return result
