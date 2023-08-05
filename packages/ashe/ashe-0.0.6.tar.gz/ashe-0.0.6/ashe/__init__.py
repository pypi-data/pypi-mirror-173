from ._dict import merge, remove
from ._list import reverse
from ._sys import size
from ._str import find
from ._date import today, yesterday, get_interval_days
from ._file import read, write


__version__ = "0.0.6"

__all__ = [
    "merge",
    "remove",
    "reverse",
    "size",
    "find",
    "read",
    "write",
    "today",
    "yesterday",
    "get_interval_days"
]
