# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QTableWidget


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class EntryTableWidget(QTableWidget):
    pass
