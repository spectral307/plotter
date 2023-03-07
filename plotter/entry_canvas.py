from matplotlib.figure import Figure
# pylint: disable-next=no-name-in-module
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT)
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from .data_header import DataHeader
from .entry import Entry


# pylint: disable-next=too-many-public-methods
class EntryCanvas(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__canvas = FigureCanvas(Figure())
        toolbar = NavigationToolbar2QT(self.__canvas, self)

        layout = QVBoxLayout(self)
        layout.addWidget(toolbar)
        layout.addWidget(self.__canvas)

        self.__axes = self.__canvas.figure.subplots()
        self.__axes.grid()
        self.__axes.set_xscale("log")

        self.__y_header = None
        self.__entry_items = {}

    def set_entries(self, entries: list[Entry], y_header: DataHeader):
        self.clear_entries()
        self.append_entries(entries)
        self.__y_header = y_header

    def set_y_header(self, y_header: DataHeader):
        if y_header != self.__y_header:
            self.__y_header = y_header
            for entryname in self.__entry_items:
                self.hide_entry(entryname, draw_idle=False)
                self.display_entry(entryname, draw_idle=True)

    def append_entries(self, entries: list[Entry]):
        for entry in entries:
            if entry.name in self.__entry_items:
                raise ValueError(
                    f"cannot append duplicate entry: {entry.name}")
            self.__entry_items[entry.name] = {}
            self.__entry_items[entry.name]["entry"] = entry
            self.__entry_items[entry.name]["line"] = None
            self.__entry_items[entry.name]["color"] = None

    def display_all_entries(self):
        for entryname in self.__entry_items:
            self.display_entry(entryname, draw_idle=False)
        self.__canvas.draw_idle()

    # pylint: disable-next=too-many-locals
    def display_entry(self, entryname: str, draw_idle: bool = True):
        if self.__entry_items[entryname]["line"] is None:
            entry = self.__entry_items[entryname]["entry"]
            x_data, y_data = entry.get_xy_data(self.__y_header)
            if self.__entry_items[entryname]["color"] is None:
                line, = self.__axes.plot(x_data, y_data)
                self.__entry_items[entryname]["color"] = line.get_color()
            else:
                color = self.__entry_items[entryname]["color"]
                line, = self.__axes.plot(x_data, y_data, color=color)
            self.__entry_items[entryname]["line"] = line
            if draw_idle:
                self.__canvas.draw_idle()

    def hide_all_entries(self):
        for entryname in self.__entry_items:
            self.hide_entry(entryname, draw_idle=False)
        self.__canvas.draw_idle()

    def hide_entry(self, entryname: str, draw_idle: bool = True):
        self.__clear_line(entryname, draw_idle)

    def clear_entries(self):
        for entryname in self.__entry_items:
            self.__clear_line(entryname, draw_idle=False)
        self.__entry_items.clear()
        self.__canvas.draw_idle()

    def __clear_line(self, entryname: str, draw_idle: bool = True):
        line = self.__entry_items[entryname]["line"]
        if line is not None:
            self.__axes.lines.remove(line)
            self.__entry_items[entryname]["line"] = None
            if draw_idle:
                self.__canvas.draw_idle()
