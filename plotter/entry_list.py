from collections.abc import Iterable
from typing import Any, Callable, Optional, overload, SupportsIndex, TypeVar
from .entry import Entry


_T = TypeVar("_T", bound=Entry)


# pylint: disable-next=too-many-public-methods
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

        self.__current_cid = 1
        self.__entries_added_handlers: dict[int,
                                            Callable[[list[_T]], None]] = {}
        self.__entries_removed_handlers: dict[int,
                                              Callable[[list[_T]], None]] = {}

    @overload
    def __setitem__(self, __i: SupportsIndex, __o: _T) -> None:
        ...

    @overload
    def __setitem__(self, __s: slice, __o: Iterable[_T]) -> None:
        ...

    def __setitem__(self, __i, __o):
        if isinstance(__o, self.__entry_type):
            self.__validate_type(__o)
            self.__validate_name(__o)
            removed_entries = [self[__i]]
            added_entries = [__o]
        elif isinstance(__o, Iterable):
            for item in __o:
                self.__validate_type(item)
                self.__validate_name(item)
            removed_entries = self[__i]
            added_entries = __o
        else:
            raise TypeError("expected __o to be of type either "
                            + f"{self.__entry_type} or "
                            + f"Iterable[{self.__entry_type}], "
                            + f"got {type(__o)}")

        ret = super().__setitem__(__i, __o)
        for handler in self.__entries_removed_handlers:
            handler(removed_entries)
        for handler in self.__entries_added_handlers:
            handler(added_entries)
        return ret

    def connect_entries_added_handler(
            self,
            handler: Callable[[list[_T]], None]
    ) -> int:
        self.__entries_added_handlers[self.__current_cid] = handler
        cid = self.__current_cid
        self.__current_cid += 1
        return cid

    def disconnect_entries_added_handler(self, cid: int) -> None:
        self.__entries_added_handlers.pop(cid, None)

    def connnect_entries_removed_handler(
            self,
            handler: Callable[[list[_T]], None]
    ) -> int:
        self.__entries_removed_handlers[self.__current_cid] = handler
        cid = self.__current_cid
        self.__current_cid += 1
        return cid

    def disconnect_entries_removed_handler(self, cid: int) -> None:
        self.__entries_removed_handlers.pop(cid, None)

    def insert(self, __index: SupportsIndex, __object: _T) -> None:
        self.__validate_type(__object)
        self.__validate_name(__object)

        ret = super().insert(__index, __object)
        added_entries = [__object]
        for handler in self.__entries_added_handlers.values():
            handler(added_entries)
        return ret

    def append(self, __object: _T) -> None:
        self.__validate_type(__object)
        self.__validate_name(__object)

        ret = super().append(__object)
        added_entries = [__object]
        for handler in self.__entries_added_handlers.values():
            handler(added_entries)
        return ret

    def extend(self, __iterable: Iterable[_T]) -> None:
        for item in __iterable:
            self.__validate_type(item)
            self.__validate_name(item)

        ret = super().extend(__iterable)
        added_entries = list(__iterable)
        for handler in self.__entries_added_handlers.values():
            handler(added_entries)
        return ret

    def clear(self) -> None:
        removed_entries: list[_T] = list(self)
        for handler in self.__entries_removed_handlers.values():
            handler(removed_entries)
        return super().clear()

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
