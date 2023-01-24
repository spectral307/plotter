# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import Qt
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import (
    QCheckBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget)


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class EntryTableWidget(QTableWidget):
    def display_entries(self, entries: list[str]):
        self.__clear()
        for entry in entries:
            self.__append_row(entry)
        self.resizeColumnsToContents()

    def __append_row(self, entry: str):
        self.insertRow(self.rowCount())

        checkbox_widget = QWidget()
        checkbox = QCheckBox(self)
        hboxlayout = QHBoxLayout(checkbox_widget)
        hboxlayout.addWidget(checkbox)
        hboxlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hboxlayout.setContentsMargins(0, 0, 0, 0)

        item = QTableWidgetItem(entry)
        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)

        self.setCellWidget(self.rowCount()-1, 0, checkbox_widget)
        self.setItem(self.rowCount()-1, 1, item)

    def __clear(self):
        self.setRowCount(0)
