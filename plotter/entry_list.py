from collections.abc import Iterable
from typing import Any, Optional, overload, SupportsIndex, TypeVar
from .entry import Entry


_T = TypeVar("_T", bound=Entry)


class EntryList(list[_T]):
    def __init__(self, iterable: Iterable[_T], entry_type: type[_T]) -> None:
        if not issubclass(entry_type, Entry):
            raise TypeError("expected entry_type of type 'Entry', "
                            + f"got '{type(entry_type)}'")
        self.__entry_type = entry_type

        for item in iterable:
            self.__validate_type(item)
            self.__validate_name(item)

        super().__init__(iterable)

    @overload
    def __setitem__(self, __i: SupportsIndex, __o: _T) -> None:
        self.__validate_type(__o)
        self.__validate_name(__o)
        super().__setitem__(__i, __o)

    @overload
    def __setitem__(self, __s: slice, __o: Iterable[_T]) -> None:
        for item in __o:
            self.__validate_type(item)
            self.__validate_name(item)
        super().__setitem__(__s, __o)

    def __setitem__(self, __i, __o):
        if isinstance(__o, self.__entry_type):
            self.__validate_type(__o)
            self.__validate_name(__o)
        elif isinstance(__o, Iterable):
            for item in __o:
                self.__validate_type(item)
                self.__validate_name(item)
        else:
            raise TypeError("expected __o to be of type either "
                            + f"{self.__entry_type} or "
                            + f"Iterable[{self.__entry_type}], "
                            + f"got {type(__o)}")

        return super().__setitem__(__i, __o)

    def insert(self, __index: SupportsIndex, __object: _T) -> None:
        self.__validate_type(__object)
        self.__validate_name(__object)
        return super().insert(__index, __object)

    def append(self, __object: _T) -> None:
        self.__validate_type(__object)
        self.__validate_name(__object)
        return super().append(__object)

    def extend(self, __iterable: Iterable[_T]) -> None:
        for item in __iterable:
            self.__validate_type(item)
            self.__validate_name(item)
        return super().extend(__iterable)

    def get_by_name(self, value: str) -> Optional[Entry]:
        for item in self:
            if item.name == value:
                return item
        return None

    def __validate_type(self, obj: Any) -> None:
        if not isinstance(obj, self.__entry_type):
            raise TypeError("expected value of type "
                            + f"'{self.__entry_type}', got '{type(obj)}'")

    def __validate_name(self, obj: _T) -> None:
        if obj.name in [entry.name for entry in self]:
            raise ValueError(
                f"cannot set value with duplicate name {obj.name}")
