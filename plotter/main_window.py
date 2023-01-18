# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QMainWindow
from .ui_main_window import Ui_MainWindow


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
