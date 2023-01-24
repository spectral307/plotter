from glob import glob
from os.path import basename, dirname, join
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import QSettings
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

    # Reason: the method will be changed and decomposed later.
    # pylint: disable-next=too-many-locals
    def open_files(self):
        caption = "Открыть файлы"
        settings = QSettings()
        directory = settings.value("last_dir")
        filefilter = "Все файлы (*.*)"
        # Reason: the variable will be used later.
        # pylint: disable-next=unused-variable
        files, _ = QFileDialog.getOpenFileNames(
            self, caption, directory, filefilter)
        if not files:
            return

        new_directory = dirname(files[0])
        if new_directory != directory:
            settings.setValue("last_dir", new_directory)

        basenames = [basename(file) for file in files]
        self.__ui.entries.display_entries(basenames)

    # Reason: the method will be changed and decomposed later.
    # pylint: disable-next=too-many-locals
    def open_folder(self):
        caption = "Открыть папку"
        settings = QSettings()
        directory = settings.value("last_dir")
        folder = QFileDialog.getExistingDirectory(  # noqa: F841
            self, caption, directory)
        if not folder:
            return

        pathname = join(folder, "*.*")
        # Reason: the variable will be used later.
        # pylint: disable-next=unused-variable
        files = glob(pathname)  # noqa: F841

        new_directory = dirname(folder)
        if new_directory != directory:
            settings.setValue("last_dir", new_directory)

        basenames = [basename(file) for file in files]
        self.__ui.entries.display_entries(basenames)
