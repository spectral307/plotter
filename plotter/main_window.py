from glob import glob
from os.path import dirname, join
# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import QSettings
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from .entry_canvas import EntryCanvas
from .frequency_response import FrequencyResponse
from .gtl_afc_excel_parser import GtlAfcExcelParser
from .ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__ui.open_files.triggered.connect(self.open_files)
        self.__ui.open_folder.triggered.connect(self.open_folder)
        self.__ui.exit_app.triggered.connect(self.exit_app)

        self.__ui.canvas = EntryCanvas()

        self.__ui.splitter.replaceWidget(1, self.__ui.canvas)

        self.__entry_type = FrequencyResponse
        self.__parser = GtlAfcExcelParser()
        self.__entries = {}

        self.__ui.entries.entry_toggled.connect(self.__handle_entry_toggled)

    def exit_app(self):
        QApplication.quit()

    # pylint: disable-next=too-many-locals
    def open_files(self):
        caption = "Открыть файлы"
        settings = QSettings()
        directory = settings.value("last_dir")
        filefilter = "Все файлы (*.*)"
        files, _ = QFileDialog.getOpenFileNames(
            self, caption, directory, filefilter)
        if not files:
            return

        new_directory = dirname(files[0])
        if new_directory != directory:
            settings.setValue("last_dir", new_directory)

        self.__entries.clear()
        entries = self.__parser.parse_files(files)
        for entry in entries:
            self.__entries[entry.name] = entry
        self.__ui.entries.set_entries(entries)
        self.__ui.canvas.set_entries(entries, self.__entry_type.y_headers[0])
        self.__ui.canvas.display_all_entries()
        self.__ui.canvas.set_y_header(self.__entry_type.y_headers[1])

    # pylint: disable-next=too-many-locals
    def open_folder(self):
        caption = "Открыть папку"
        settings = QSettings()
        directory = settings.value("last_dir")
        folder = QFileDialog.getExistingDirectory(
            self, caption, directory)
        if not folder:
            return

        pathname = join(folder, "*.*")
        files = glob(pathname)

        new_directory = dirname(folder)
        if new_directory != directory:
            settings.setValue("last_dir", new_directory)

        self.__entries.clear()
        entries = self.__parser.parse_files(files)
        for entry in entries:
            self.__entries[entry.name] = entry

        self.__entries.clear()
        entries = self.__parser.parse_files(files)
        for entry in entries:
            self.__entries[entry.name] = entry
        self.__ui.entries.set_entries(entries)
        self.__ui.canvas.set_entries(entries, self.__entry_type.y_headers[0])
        self.__ui.canvas.display_all_entries()
        self.__ui.canvas.set_y_header(self.__entry_type.y_headers[1])

    def __handle_entry_toggled(self, entryname, checked):
        if checked:
            self.__ui.canvas.display_entry(entryname)
        else:
            self.__ui.canvas.hide_entry(entryname)
