# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from .ui_main_window import Ui_MainWindow


# Reason: more public methods will be added later.
# pylint: disable-next=too-few-public-methods
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__ui.open_files.triggered.connect(self.open_files)
        self.__ui.open_folder.triggered.connect(self.open_folder)
        self.__ui.exit_app.triggered.connect(self.exit_app)

    def exit_app(self):
        QApplication.quit()

    def open_files(self):
        caption = "Открыть файлы"
        directory = "/"
        filefilter = "Все файлы (*.*)"
        # Reason: the variable will be used later.
        # pylint: disable-next=unused-variable
        filenames, _ = QFileDialog.getOpenFileNames(
            self, caption, directory, filefilter)

    def open_folder(self):
        caption = "Открыть папку"
        directory = "/"
        # Reason: the variable will be used later.
        # pylint: disable-next=unused-variable
        folder = QFileDialog.getExistingDirectory(  # noqa: F841
            self, caption, directory)
