import logging
from dataclasses import dataclass
from typing import Optional

import rich

from timetable_cli.app import App
from timetable_cli.utils import tag

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@dataclass
class Quote:
    text: str
    author: Optional[str] = None
    year: Optional[str] = None

    def show(self, app: App):
        text = f'"{self.text}"'
        if self.author:
            text += f" - {self.author}"
            if self.year:
                text += ", "
        if self.year:
            text += str(self.year)
        rich.print(tag(text, app.colorscheme["quote_text"]))
