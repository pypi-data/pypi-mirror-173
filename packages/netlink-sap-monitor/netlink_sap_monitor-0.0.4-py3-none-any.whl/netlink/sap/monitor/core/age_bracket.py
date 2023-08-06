import datetime
from collections import defaultdict
from netlink.core import Mapping

from netlink.logging import logger


class AgeBracket(Mapping):
    def __init__(self, brackets=None):
        logger.debug('Initializing AgeBracket ({id(self)})')
        if brackets is None:
            brackets = {
                datetime.timedelta(minutes=5): "d00h00m05",
                datetime.timedelta(minutes=15): "d00h00m15",
                datetime.timedelta(minutes=30): "d00h00m30",
                datetime.timedelta(hours=1): "d00h01",
                datetime.timedelta(hours=2): "d00h02",
                datetime.timedelta(hours=4): "d00h04",
                datetime.timedelta(hours=12): "d00h12",
                datetime.timedelta(days=1): "d01",
                datetime.timedelta(days=2): "d02",
                datetime.timedelta(days=7): "d07",
                datetime.timedelta(days=28): "d28",
                datetime.timedelta(days=99999): "d99999",
            }
        logger.trace(f'Brackets: {brackets}')
        self._brackets = brackets
        self._thresholds = sorted(self._brackets.keys())
        self._data = defaultdict(list)

    def add(self, age: datetime.timedelta, item):
        for threshold in self._thresholds:
            if age <= threshold:
                logger.trace(f'Item {item!r} added to bracket {self._brackets[threshold]} ({id(self)})')
                self._data[self._brackets[threshold]].append(item)
                return

    def clear(self):
        logger.debug(f'Cleared AgeBracket ({id(self)})')
        self._data.clear()
