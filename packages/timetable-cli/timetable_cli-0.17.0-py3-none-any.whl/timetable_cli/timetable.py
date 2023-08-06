from dataclasses import dataclass
import datetime
import logging
from typing import List

from timetable_cli.activity import Activity
from timetable_cli.category import ActivityCategory

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Timetable:
    """Activities list."""
    activities: List[Activity]

    @property
    def categories(self) -> List[ActivityCategory]:
        result = []
        for activity in self.activities:
            category = activity.category
            if category:
                if category not in result:
                    result.append(category)
        return result

    def for_datetime(self, input_datetime: datetime.datetime):
        result = None
        for i, activity in enumerate(self.activities):
            if i == 0:
                result = self.activities[-1]
                continue
            if i == len(self.activities) - 1:
                return activity
            if activity.start > input_datetime:
                return result
            result = activity

    def centered(self, activity) -> List[Activity]:
        index = self.activities.index(activity)
        return self.activities[index:] + self.activities[:index]

    def __str__(self) -> str:
        return f"Timetable(activities: {len(self.activities)})"

    def __repr__(self) -> str:
        return self.__str__()

    def __post__init__(self):
        self.activities.sort(key=lambda x: x.start)
