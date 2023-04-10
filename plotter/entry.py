from os.path import basename, splitext
import pandas as pd
from .data_header import DataHeader


class Entry:
    x_header: DataHeader
    y_headers: tuple[DataHeader, ...]

    def __init__(self, name: str, data: pd.DataFrame):
        self.name = name
        self.data = data

    @classmethod
    # pylint: disable-next=too-many-locals, too-many-arguments
    def from_excel_columns(cls,
                           file: str,
                           sheet: str,
                           column_mapping: dict[DataHeader, str],
                           header: int = 0,
                           name: str = "auto") \
            -> "Entry":
        file_basename = basename(file)
        root, ext = splitext(file_basename)

        if ext not in (".xlsx", ".xlsm"):
            raise ValueError(f"Excel file expected, got: {ext}")

        if not name:
            raise ValueError("'name' is invalid")
        if name == "auto":
            name = root

        usecols = column_mapping[cls.x_header]
        names = [cls.x_header]
        for y_header in cls.y_headers:
            usecols += f",{column_mapping[y_header]}"
            names.append(y_header)

        data = pd.read_excel(
            file,
            sheet_name=sheet,
            header=header,
            usecols=usecols,
            names=names)

        return cls(name, data)

    def get_xy_data(self, y_header: DataHeader) -> tuple[pd.Series, pd.Series]:
        if y_header not in self.y_headers:
            raise ValueError(f"no such y_header in entry: {y_header}")
        return self.data[self.x_header], self.data[y_header]
