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
    # pylint: disable-next=too-many-locals
    def from_excel(cls, file: str, sheet: str,
                   column_mapping: dict[DataHeader, str], name=None) \
            -> "Entry":
        file_basename = basename(file)
        root, ext = splitext(file_basename)

        if ext not in (".xlsx", ".xlsm"):
            raise ValueError(f"Excel file expected, got: {ext}")

        if name is None:
            name = root

        usecols = column_mapping[cls.x_header]
        names = [cls.x_header]
        for header in cls.y_headers:
            usecols += f",{column_mapping[header]}"
            names.append(header)

        data = pd.read_excel(
            file,
            sheet_name=sheet,
            usecols=usecols,
            names=names)

        return cls(name, data)

    def get_xy_data(self, y_header: DataHeader) -> tuple[pd.Series, pd.Series]:
        if y_header not in self.y_headers:
            raise ValueError(f"y_header isn't in entry: {y_header}")
        return self.data[self.x_header], self.data[y_header]
