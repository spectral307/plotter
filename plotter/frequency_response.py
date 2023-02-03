import pandas as pd
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

    def get_xy_data(self, y_header: DataHeader) -> tuple[pd.Series, pd.Series]:
        if y_header not in FrequencyResponse.y_headers:
            raise ValueError(f"No such DataHeader in entry: {y_header}.")
        return self.data[FrequencyResponse.x_header], self.data[y_header]
