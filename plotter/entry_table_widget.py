# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import Qt
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QCheckBox, QTableWidget, QTableWidgetItem


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class EntryTableWidget(QTableWidget):
    def display_entries_in_entries_table(self, entries: list[str]):
        self.__clear_entries_table()
        for entry in entries:
            self.__append_row_to_entries_table(entry)

    def __append_row_to_entries_table(self, entry: str):
        item = QTableWidgetItem(entry)

        self.insertRow(self.rowCount())
        self.setCellWidget(self.rowCount()-1, 0, QCheckBox(self))
        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.setItem(self.rowCount()-1, 1, item)

    def __clear_entries_table(self):
        self.setRowCount(0)
