from matplotlib.figure import Figure
# Reason: matplotlib is a third party module.
# pylint: disable-next=no-name-in-module
from matplotlib.backends.backend_qtagg import FigureCanvas


class EntryCanvas(FigureCanvas):
    def __init__(self):
        super().__init__(Figure())
        self.__axes = self.figure.subplots()
        self.__axes.grid()
        self.__lines = {}

    def plot(self, entryname, *args, **kwargs):
        line, = self.__axes.plot(*args, **kwargs)
        self.__lines[entryname] = line
        self.draw_idle()

    def clear(self):
        for line in list(self.__lines.values()):
            self.__axes.lines.remove(line)
        self.__lines.clear()
        self.draw_idle()

    def clear_line(self, entryname):
        line = self.__lines.pop(entryname)
        self.__axes.lines.remove(line)
        self.draw_idle()
