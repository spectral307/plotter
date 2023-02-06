# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import Qt, pyqtSignal
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import (
    QCheckBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget)


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class EntryTableWidget(QTableWidget):
    entry_toggled = pyqtSignal(str, bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__entries = {}

    def set_entries(self, entries: list[str]):
        self.__clear()
        try:
            for entry in entries:
                self.__append_row(entry)
        except ValueError:
            self.__clear()
            raise
        self.resizeColumnsToContents()

    def __append_row(self, entry: str):
        if entry in self.__entries:
            raise ValueError(f"cannot insert duplicate entry: {entry}")

        initial_check_state = False
        self.__entries[entry] = initial_check_state

        self.insertRow(self.rowCount())

        checkbox = self.__append_checkbox()
        checkbox.setObjectName(entry)
        checkbox.setChecked(initial_check_state)
        checkbox.toggled.connect(  # type: ignore[attr-defined]
            lambda checked: self.__handle_checkbox_toggled(entry, checked))

        item = self.__append_item()
        item.setText(entry)

    def __append_checkbox(self) -> QCheckBox:
        checkbox_widget = QWidget(self)
        checkbox = QCheckBox(checkbox_widget)
        hboxlayout = QHBoxLayout(checkbox_widget)
        hboxlayout.addWidget(checkbox)
        hboxlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(self.rowCount()-1, 0, checkbox_widget)
        return checkbox

    def __append_item(self) -> QTableWidgetItem:
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.setItem(self.rowCount()-1, 1, item)
        return item

    def __handle_checkbox_toggled(self, entry, checked):
        self.__entries[entry] = checked
        self.entry_toggled.emit(entry, checked)

    def __clear(self):
        self.setRowCount(0)
        self.__entries.clear()
