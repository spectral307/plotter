from glob import glob
from os.path import join
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from matplotlib.figure import Figure
# Reason: matplotlib is a third party module.
# pylint: disable-next=no-name-in-module
from matplotlib.backends.backend_qtagg import FigureCanvas
from .ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__ui.open_files.triggered.connect(self.open_files)
        self.__ui.open_folder.triggered.connect(self.open_folder)
        self.__ui.exit_app.triggered.connect(self.exit_app)

        self.__ui.canvas = FigureCanvas(Figure())
        self.__axes = self.__ui.canvas.figure.subplots()
        self.__axes.grid()

        self.__ui.splitter.replaceWidget(1, self.__ui.canvas)

    def exit_app(self):
        QApplication.quit()

    def open_files(self):
        caption = "Открыть файлы"
        directory = "/"
        filefilter = "Все файлы (*.*)"
        # Reason: the variable will be used later.
        # pylint: disable-next=unused-variable
        files, _ = QFileDialog.getOpenFileNames(
            self, caption, directory, filefilter)

    def open_folder(self):
        caption = "Открыть папку"
        directory = "/"
        folder = QFileDialog.getExistingDirectory(  # noqa: F841
            self, caption, directory)
        pathname = join(folder, "*.*")
        # Reason: the variable will be used later.
        # pylint: disable-next=unused-variable
        files = glob(pathname)  # noqa: F841
