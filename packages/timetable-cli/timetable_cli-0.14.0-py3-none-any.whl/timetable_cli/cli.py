import imp
import json
import logging
import os
import platform
import random
import re
import sqlite3
import subprocess
import sys
from time import sleep
from typing import List, Optional

import click
import interactive_select
import rich
from appdirs import AppDirs
from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table

from timetable_cli import selectors
from timetable_cli.activity import Activity, ActivityStatus
from timetable_cli.application import (Application, CategoriesRenderConfig,
                                       RenderConfig, TableConfig)
from timetable_cli.enums import Columns
from timetable_cli.render import (DEFAULT_COLUMNS_STR, get_activity_prop_str,
                                  show_activities_table)
from timetable_cli.selectors import parse_selectors
from timetable_cli.timetable import Timetable
from timetable_cli.utils import parse_timedelta_str

appdirs = AppDirs(appname="timetable_cli")
_default_config_dir = appdirs.user_config_dir
_default_config_file = os.path.join(_default_config_dir, "config.py")
_default_state_dir = appdirs.user_state_dir
_default_db = os.path.join(_default_state_dir, "db.sqlite3")

COMMANDS = ["show_date", "show_quotes",
            "show_status", "show_activities", "show_rules"]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _get_db_connection(db_filename: str, debug: bool) -> sqlite3.Connection:
    connection = sqlite3.connect(
        db_filename, detect_types=sqlite3.PARSE_DECLTYPES
        | sqlite3.PARSE_COLNAMES
    )
    cursor = connection.cursor()
    cursor.executescript(
        """
CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    variation VARCHAR(255),
    start TIMESTAMP
);

CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status INTEGER NOT NULL,
    date TIMESTAMP,
    activity INTEGER,
    FOREIGN KEY (activity) REFERENCES Activities(id)
);
"""
    )
    connection.commit()
    if debug:
        connection.set_trace_callback(print)
    return connection


@click.command()
@click.option("--config", default=_default_config_file, help="Config module")
@click.option("--db", default=_default_db, help="Database file.")
@click.option("--debug", default=False, is_flag=True, help="Show debug info.")
@click.option("--add-empty-lines", default=False, is_flag=True)
@click.option("--clear-screen", default=False, is_flag=True)
@click.option("--default-activities-selectors", default="..")
@click.option("-d", "--global-timedelta", default="")
@click.option("-D", "--show-date", is_flag=True, default=False, help="Show current date and time.")
@click.option("-S", "--show-status", is_flag=True, default=False, help="Show info about current and next activities.")
@click.option("--max-status-length", type=int, default=None)
@click.option("-A", "--show-activities", is_flag=True, default=False, help="Show activities table filtered by activities_selectors.")
@click.argument("activities_selector", nargs=-1, type=str)
@click.option("--list-categories", is_flag=True, default=False, help="Show activities categories when rendering activities table.")
@click.option("-c", "--columns", default=DEFAULT_COLUMNS_STR, help="Columns to display when rendering activities table.")
@click.option("--table-kwargs", default="{}", help="Activities table kwargs (json)")
@click.option("--ignore-time-status", is_flag=True, default=False)
@click.option("--combine-title-and-variation", is_flag=True, default=False, help="Append activity variation to title when rendering activities table.")
@click.option("-R", "--show-rules", is_flag=True, default=False, help="Show random rule.")
@click.option("-r", "--rules-list", default=False, is_flag=True, help="Show rules table instead of random rule.")
@click.option("-Q", "--show-quotes", is_flag=True, default=False, help="Show random quote.")
@click.option("-q", "--quotes-list", default=False, is_flag=True, help="Show quotes table instead of random quote.")
@click.option("-W", "--watch", is_flag=True, default=False)
@click.option("--watch-interval", default=5)
@click.option("--watch-notification", default=False, is_flag=True)
@click.option("--watch-notification-text", default="timetable-cli")
@click.option("--watch-notification-cmd", default="notify-send --expire-time 60000")
@click.option("--watch-voice", default=False, is_flag=True)
@click.option("--watch-voice-cmd", default="espeak -s 0.1 -g 5 -p 1")
@click.option("--watch-notify-eta", default="120m 60m 30m")
@click.option("-C", "--check-activities", default=None, type=str, required=False, help="Check activities.")
@click.option("-I", "--check-activities-interactively", default=False, is_flag=True, help="Check activities interactively.")
@click.option("-c", "--check-activities-already-checked", default=False, is_flag=True, help="Check already checked activities.")
@click.option("-e", "--edit-config", default=False, is_flag=True, help="Edit config module.")
@click.option("--editor", default=os.environ.get("EDITOR", "vim"), help="Text editor.")
@click.option("--edit-db", default=False, is_flag=True, help="Edit database.")
@click.pass_context
def cli(context: click.Context, activities_selector: List[str], **kwargs):
    if kwargs["debug"]:
        logging.basicConfig(level=logging.DEBUG)
        logger.debug(context)
        logger.debug(activities_selector)
        logger.debug(kwargs)
    if not activities_selector and kwargs["default_activities_selectors"]:
        activities_selector = kwargs["default_activities_selectors"].split()

    if kwargs["edit_config"]:
        subprocess.call(kwargs["editor"].split() + [kwargs['config']])
        sys.exit()
    if kwargs["edit_db"]:
        subprocess.call(f"xdg-open {kwargs['db']}".split())
        sys.exit()

    app = Application.from_config_module(
        config_module=imp.load_source(
            "config_module", kwargs["config"]),
        connection=_get_db_connection(kwargs["db"], kwargs["debug"]),
        global_timedelta=parse_timedelta_str(
            kwargs["global_timedelta"]),
        table_config=TableConfig(
            table_kwargs=json.loads(kwargs["table_kwargs"]),
            columns=Columns.parse_str(kwargs["columns"]),
        ),
        render_config=RenderConfig(
            ignore_time_status=kwargs["ignore_time_status"],
            combine_title_and_variation=kwargs["combine_title_and_variation"],
        ),
        categories_render_config=CategoriesRenderConfig(
            list_categories=kwargs["list_categories"],
        ),
    )
    context.obj = app

    try:
        selectors.ShortcutSelector.shortcuts.update(
            app.config_module.get_shortcuts())
    except AttributeError:
        pass

    if kwargs["clear_screen"]:
        clear_screen()
    activities = select_activities(app, activities_selector)

    if not kwargs["check_activities_already_checked"]:
        activities_to_check = []
        for activity in activities:
            activity_status_index = app.activity_status_variations.index(
                    activity.get_status(app))
            if activity_status_index == 0:
                activities_to_check.append(activity)
    else:
        activities_to_check = activities

    logger.debug("activities_to_check: %s", activities_to_check)

    if kwargs["check_activities_interactively"]:
        if kwargs["check_activities"]:
            raise ValueError
        check_activities_interactively(app, activities_to_check, **kwargs)
    if kwargs["check_activities"]:
        status = None
        for index, variation in enumerate(app.activity_status_variations):
            try:
                if index == int(kwargs["check_activities"]):
                    status = variation
                    break
            except ValueError:
                if re.match(kwargs["check_activities"].lower(), variation.title.lower()):
                    status = variation
                    break
        if not status:
            raise ValueError
        logger.debug("status: %s", status)
        if kwargs["watch"]:
            raise ValueError
        check_activities(app, activities_to_check, status)

    if kwargs["watch"]:
        watch(app, activities, **kwargs)
    else:
        show_info(app, activities, **kwargs)


def check_activities_interactively(app, activities: List[Activity], **kwargs):
    for activity in activities:
        print(kwargs)
        if kwargs["clear_screen"]:
            clear_screen()
        show_activities_table([activity], app, app.table_config, app.render_config, app.categories_render_config, show_header=False)
        status = app.activity_status_variations[interactive_select.select(
            ["none", "ok", "skip"], min_items=1, max_items=1, retry=True)[0]]
        activity.set_status(app, status)


def check_activities(app, activities: List[Activity], status: ActivityStatus):
    for activity in activities:
        activity.set_status(app, status)


def watch(app: Application, activities: List[Activity], **kwargs):
    """Render in a loop and display notifications."""
    previous_activity = app.timetable.for_datetime(app.now())
    while True:
        current_activity = app.timetable.for_datetime(app.now())
        if kwargs["clear_screen"]:
            clear_screen()
        show_info(app, activities, **kwargs)
        if previous_activity != current_activity:
            next_activity = current_activity.next()
            text = kwargs["watch_notification_text"]
            title = current_activity.title
            if current_activity.variation:
                title += " " + current_activity.variation
            if kwargs["watch_notify_eta"]:
                if current_activity != app.timetable[-1]:
                    eta = next_activity.eta(app)
                    if eta in kwargs["watch_notify_eta"].split():
                        if kwargs["watch_notification"]:
                            command = kwargs["watch_notification_cmd"
                                             ].split()
                            command.extend(
                                [f'"{text}"',
                                    f'"{title}, ETA is {eta}"']
                            )
                            subprocess.call(command)
                        if kwargs["watch_voice"]:
                            command = kwargs["watch_voice_cmd"].split(
                            )
                            command.extend(
                                [f'"{text} says {title}, ETA is {eta}"'])
                            subprocess.call(command)
            if previous_activity != current_activity:
                if kwargs["watch_notification"]:
                    command = kwargs["watch_notification_cmd"].split(
                    )
                    command.extend([f'"{text}"', f'"{title}"'])
                    subprocess.call(command)
                if kwargs["watch_voice"]:
                    command = kwargs["watch_voice_cmd"].split()
                    command.extend([f'"{text} says {title}"'])
                    subprocess.call(command)
        previous_activity = current_activity
        sleep(kwargs["watch_interval"])


def show_info(app: Application, activities: List[Activity], **kwargs):
    """Show info about timetable."""
    kwargs_filtered = {
        key: val for key, val in kwargs.items() if key in COMMANDS and val
    }
    for index, (key, val) in enumerate(kwargs_filtered.items()):
        if not val:
            continue
        match key:
            case "show_date":
                show_time_and_date(app)
            case "show_quotes":
                if kwargs["quotes_list"]:
                    show_quotes(app)
                else:
                    show_random_quote(app)
            case "show_status":
                show_status(app, app.timetable, kwargs["max_status_length"])
            case "show_activities":
                show_activities(app, activities)
            case "show_rules":
                if kwargs["rules_list"]:
                    show_rules(app)
                else:
                    show_random_rule(app)
        if kwargs["add_empty_lines"] and index != len(kwargs_filtered) - 1:
            rich.print("")


def select_activities(app, selectors_str_list: List[str]) -> List[Activity]:
    timetable = app.timetable
    selectors = parse_selectors(selectors_str_list)
    logger.debug(selectors)
    activities = []
    for selector in selectors:
        activities += selector.get(timetable, app.now())
    logger.debug(activities)
    return activities


def show_activities(app: Application, activities: List[Activity]):
    """Show activities table."""
    show_activities_table(
        activities,
        app,
        app.table_config,
        app.render_config,
        app.categories_render_config,
    )


def show_time_and_date(app: Application):
    """Show current time and date."""
    table = Table(
        # show_edge=False,
        show_header=False,
        box=ROUNDED,
    )
    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    time = app.now().time()
    date = app.now().date()
    table.add_row(time.isoformat()[
                  :5], week_days[date.weekday()], date.isoformat())
    rich.print(table)


def show_status(
        app: Application,
        timetable: Timetable,
        max_status_length: Optional[int] = None
                ):
    """Show current and next activities."""
    activity_1 = timetable.for_datetime(app.now())
    activity_2 = activity_1.next()
    a1_title = get_activity_prop_str(
        activity_1, Columns.TITLE, app, app.render_config
    ).strip()
    a2_title = get_activity_prop_str(
        activity_2, Columns.TITLE, app, app.render_config
    ).strip()
    a2_eta = get_activity_prop_str(
        activity_2, Columns.ETA, app, app.render_config
    ).strip()
    table = Table(show_header=False, show_edge=False, box=ROUNDED)
    table.add_row(
        # app.now().time().isoformat()[:5],
        a1_title,
        "ETA " + a2_eta,
        a2_title,
    )
    console = Console()
    with console.capture() as capture:
        console.print(table)
    line = capture.get()
    if max_status_length:
        if len(line) > max_status_length - 3:
            line = line[:max_status_length - 3] + "..."
    print(line.removesuffix("\n"))


def show_random_rule(app: Application):
    """Show one random rule."""
    rules = app.rules
    if not rules:
        return
    index = random.randint(0, len(rules) - 1)
    rich.print(rules[index])


def show_rules(app: Application):
    """Show all rules."""
    rules = app.rules
    if not rules:
        return
    table = Table(show_header=False, box=ROUNDED)
    for rule in rules:
        table.add_row(rule)
    rich.print(table)


def show_random_quote(app: Application):
    """Show one random quote."""
    quotes = app.quotes
    if not quotes:
        return
    index = random.randint(0, len(quotes) - 1)
    quote = quotes[index]
    quote.show(app)


def show_quotes(app: Application):
    """Show all quotes."""
    quotes = app.quotes
    if not quotes:
        return
    table = Table(box=ROUNDED)
    table.add_column("Quote")
    table.add_column("Author")
    table.add_column("Year")
    for quote in quotes:
        table.add_row(quote.text, quote.author, str(quote.year))
    rich.print(table)


def clear_screen():
    """Clears screen."""
    if platform.system() == "Linux":
        subprocess.call("clear")
    else:
        raise ValueError
