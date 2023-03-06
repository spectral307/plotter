from collections.abc import Iterable
from typing import TypeVar
from .entry import Entry


_T = TypeVar("_T", bound=Entry)


class EntryList(list[_T]):
    def __init__(self, iterable: Iterable[_T]) -> None:
        super().__init__(iterable)
