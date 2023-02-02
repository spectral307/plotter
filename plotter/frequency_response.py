import pandas as pd
from .header import Header


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class FrequencyResponse:
    x_header = Header("Frequency", "F", "E", "Hz")
    y_headers = (Header("Sensitivity absolute", "S(abs)", "F"),
                 Header("Sensitivity relative", "S(rel)", "G", "%"))

    def __init__(self, name: str, data: pd.DataFrame):
        self.name = name
        self.data = data

    def get_xy_data(self, y_header: Header) -> tuple[pd.Series, pd.Series]:
        if y_header not in FrequencyResponse.y_headers:
            raise ValueError(f"No such header in entry: {y_header}.")
        return self.data[FrequencyResponse.x_header], self.data[y_header]
