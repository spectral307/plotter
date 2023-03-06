from .data_header import DataHeader
from .entry import Entry


# pylint: disable-next=too-few-public-methods
class FrequencyResponse(Entry):
    x_header: DataHeader = DataHeader("Frequency", "F", "Hz")
    y_headers: tuple[DataHeader, ...] = (
        DataHeader("Sensitivity absolute", "S(abs)"),
        DataHeader("Sensitivity relative", "S(rel)", "%")
    )
