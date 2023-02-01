from os.path import basename
import pandas as pd


class GtlAfcReportEntries(dict):
    @classmethod
    def create(cls, files: list[str]) -> "GtlAfcReportEntries":
        entries = cls()

        for file in files:
            file_basename = basename(file)
            dataframe = pd.read_excel(file, "data", usecols="E:G")
            entries[file_basename] = dataframe

        return entries
