from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DataHeader:
    name: str
    short_name: str
    excel_col: str
    unit: Optional[str] = None
    description: Optional[str] = None

    def __repr__(self) -> str:
        ret = self.short_name
        if self.unit is not None:
            ret += f", {self.unit}"
        return ret
