from os.path import basename
import pandas as pd
from .gtl_afc_report_entry import GtlAfcReportEntry


class GtlAfcReportEntries(list):
    @classmethod
    def create(cls, files: list[str]) -> "GtlAfcReportEntries":
        entries = cls()

        for file in files:
            entry_name = basename(file)
            data = pd.read_excel(
                file,
                sheet_name="data",
                usecols=(f"{GtlAfcReportEntry.x_header.excel_col}"
                         + f",{GtlAfcReportEntry.y_headers[0].excel_col}"
                         + f",{GtlAfcReportEntry.y_headers[1].excel_col}"),
                names=[GtlAfcReportEntry.x_header,
                       GtlAfcReportEntry.y_headers[0],
                       GtlAfcReportEntry.y_headers[1]]
            )

            entry = GtlAfcReportEntry(entry_name, data)
            entries.append(entry)

        return entries
