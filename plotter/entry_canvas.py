from typing import Any
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
    def __init__(self, *args, initial_show_state: bool = True, **kwargs):
        super().__init__(*args, **kwargs)

        self.__initial_show_state = initial_show_state

        self.__canvas = FigureCanvas(Figure())
        toolbar = NavigationToolbar2QT(self.__canvas, self)

        layout = QVBoxLayout(self)
        layout.addWidget(toolbar)
        layout.addWidget(self.__canvas)

        self.__axes = self.__canvas.figure.subplots()
        self.__axes.grid()
        self.__axes.set_xscale("log")

        self.__y_header: Any = None
        self.__entries: dict[Entry, dict[str, Any]] = {}

    def set_entries(self, entries: list[Entry], y_header: DataHeader):
        self.clear_entries()
        self.__y_header = y_header
        self.append_entries(entries)

    def set_y_header(self, y_header: DataHeader):
        if y_header != self.__y_header:
            self.__y_header = y_header
            for entry in self.__entries:
                self.__clear_entry_line(entry, draw_idle=False)
                self.__plot_entry_line(entry, draw_idle=True)

    def append_entries(self, entries: list[Entry]):
        if self.__y_header is None:
            self.__y_header = entries[0].y_headers[0]
        for entry in entries:
            self.__entries[entry] = {}
            self.__entries[entry]["line"] = None
            self.__entries[entry]["color"] = None
            self.__entries[entry]["is_shown"] = self.__initial_show_state
            if self.__initial_show_state:
                self.__plot_entry_line(entry, draw_idle=True)

    def show_all_entries(self):
        for entry in self.__entries:
            self.show_entry(entry, draw_idle=False)
        self.__canvas.draw_idle()

    def show_entry(self, entry: Entry, draw_idle: bool = True):
        self.__plot_entry_line(entry, draw_idle=draw_idle)

    def hide_all_entries(self):
        for entry in self.__entries:
            self.hide_entry(entry, draw_idle=False)
        self.__canvas.draw_idle()

    def hide_entry(self, entry: Entry, draw_idle: bool = True):
        self.__clear_entry_line(entry, draw_idle)

    def clear_entries(self):
        for entry in self.__entries:
            self.__clear_entry_line(entry, draw_idle=False)
        self.__entries.clear()
        self.__canvas.draw_idle()

    # pylint: disable-next=too-many-locals
    def __plot_entry_line(self, entry: Entry, draw_idle: bool = True):
        if self.__entries[entry]["line"] is None:
            if self.__y_header is None:
                raise AttributeError()
            x_data, y_data = entry.get_xy_data(self.__y_header)
            if self.__entries[entry]["color"] is None:
                line, = self.__axes.plot(x_data, y_data)
                self.__entries[entry]["color"] = line.get_color()
            else:
                color = self.__entries[entry]["color"]
                line, = self.__axes.plot(x_data, y_data, color=color)
            self.__entries[entry]["line"] = line
            if draw_idle:
                self.__canvas.draw_idle()

    def __clear_entry_line(self, entry: Entry, draw_idle: bool = True):
        line = self.__entries[entry]["line"]
        if line is not None:
            self.__axes.lines.remove(line)
            self.__entries[entry]["line"] = None
            if draw_idle:
                self.__canvas.draw_idle()
