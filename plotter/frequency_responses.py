from os.path import basename
import pandas as pd
from .frequency_response import FrequencyResponse


class FrequencyResponses(list):
    @classmethod
    def create(cls, files: list[str]) -> "FrequencyResponses":
        entries = cls()

        for file in files:
            entry_name = basename(file)
            data = pd.read_excel(
                file,
                sheet_name="data",
                usecols=(f"{FrequencyResponse.x_header.excel_col}"
                         + f",{FrequencyResponse.y_headers[0].excel_col}"
                         + f",{FrequencyResponse.y_headers[1].excel_col}"),
                names=[FrequencyResponse.x_header,
                       FrequencyResponse.y_headers[0],
                       FrequencyResponse.y_headers[1]]
            )

            entry = FrequencyResponse(entry_name, data)
            entries.append(entry)

        return entries

    def append_from_files(self, files: list[str]):
        for file in files:
            entry_name = basename(file)
            data = pd.read_excel(
                file,
                sheet_name="data",
                usecols=(f"{FrequencyResponse.x_header.excel_col}"
                         + f",{FrequencyResponse.y_headers[0].excel_col}"
                         + f",{FrequencyResponse.y_headers[1].excel_col}"),
                names=[FrequencyResponse.x_header,
                       FrequencyResponse.y_headers[0],
                       FrequencyResponse.y_headers[1]]
            )

            entry = FrequencyResponse(entry_name, data)
            self.append(entry)
