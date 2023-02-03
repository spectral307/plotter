import pandas as pd
from os.path import basename, splitext
from .data_header import DataHeader
from .entry import Entry


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class FrequencyResponse(Entry):
    x_header = DataHeader("Frequency", "F", "Hz")
    y_headers = (DataHeader("Sensitivity absolute", "S(abs)"),
                 DataHeader("Sensitivity relative", "S(rel)", "%"))

    def __init__(self, name: str, data: pd.DataFrame):
        self.name = name
        self.data = data

    @classmethod
    def from_excel(self, file: str, sheet: str,
                   column_mapping: dict[DataHeader, str], name=None) \
            -> "FrequencyResponse":
        file_basename = basename(file)
        root, ext = splitext(file_basename)

        if ext != ".xlsx" or ext != ".xlsm":
            raise ValueError(f"excel file expected, got '{ext}'")

        if name is None:
            name = root

        usecols = column_mapping[FrequencyResponse.x_header]
        names = [FrequencyResponse.x_header]
        for header in FrequencyResponse.y_headers:
            usecols += f",{column_mapping[header]}"
            names.append(header)

        data = pd.read_excel(
            file,
            sheet_name=sheet,
            usecols=usecols,
            names=names)

        return FrequencyResponse(name, data)

    def get_xy_data(self, y_header: DataHeader) -> tuple[pd.Series, pd.Series]:
        if y_header not in FrequencyResponse.y_headers:
            raise ValueError(f"No such DataHeader in entry: {y_header}.")
        return self.data[FrequencyResponse.x_header], self.data[y_header]
