from .entry import Entry
from .frequency_response import FrequencyResponse
from .parser import Parser


class GtlAfcExcelParser(Parser):
    def parse_file(self, file: str) -> list[Entry]:
        column_mapping = {
            FrequencyResponse.x_header: "E",
            FrequencyResponse.y_headers[0]: "F",
            FrequencyResponse.y_headers[1]: "G"
        }
        return [FrequencyResponse.from_excel(file, "data", column_mapping)]

    def parse_files(self, files: list[str]) -> list[Entry]:
        return [self.parse_file(file)[0] for file in files]
