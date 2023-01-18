from .ui_main_window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
