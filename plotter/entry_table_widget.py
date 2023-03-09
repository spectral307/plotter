# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import Qt, pyqtSignal
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import (
    QCheckBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget)
from .entry import Entry


# pylint: disable-next=too-few-public-methods
class EntryTableWidget(QTableWidget):
    entry_toggled = pyqtSignal(str, bool)

    def __init__(self, *args, initial_check_state: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_check_state: bool = initial_check_state
        self.__check_states: dict[str, bool] = {}

    def set_entries(self, entries: list[Entry]):
        self.__clear()
        self.append_entries(entries)

    def append_entries(self, entries: list[Entry]):
        for entry in entries:
            self.__append_entry(entry)
        self.resizeColumnsToContents()

    def __append_entry(self, entry: Entry):
        self.__check_states[entry.name] = self.__initial_check_state

        self.insertRow(self.rowCount())

        checkbox = self.__append_checkbox()
        checkbox.setObjectName(entry.name)
        checkbox.setChecked(self.__check_states[entry.name])
        checkbox.toggled.connect(  # type: ignore[attr-defined]
            lambda checked: self.__handle_checkbox_toggled(entry.name,
                                                           checked))

        item = self.__append_table_widget_item()
        item.setText(entry.name)

    def __append_checkbox(self) -> QCheckBox:
        checkbox_widget = QWidget(self)
        checkbox = QCheckBox(checkbox_widget)
        hboxlayout = QHBoxLayout(checkbox_widget)
        hboxlayout.addWidget(checkbox)
        hboxlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(self.rowCount()-1, 0, checkbox_widget)
        return checkbox

    def __append_table_widget_item(self) -> QTableWidgetItem:
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.setItem(self.rowCount()-1, 1, item)
        return item

    def __handle_checkbox_toggled(self, entryname: str, checked: bool):
        self.__check_states[entryname] = checked
        self.entry_toggled.emit(entryname, checked)

    def __clear(self):
        self.setRowCount(0)
        self.__check_states.clear()
