# Reason: matplotlib is a third party module.
# pylint: disable-next=no-name-in-module
from matplotlib.backends.backend_qtagg import FigureCanvas


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class EntryCanvas(FigureCanvas):
    pass
