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
from .entry import Entry
from .entry_list import EntryList


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)

        self.__ui.open_files.triggered.connect(self.open_files)
        self.__ui.open_folder.triggered.connect(self.open_folder)
        self.__ui.add_files.triggered.connect(self.add_files)
        self.__ui.add_folder.triggered.connect(self.add_folder)
        self.__ui.exit_app.triggered.connect(self.exit_app)

        self.__ui.canvas = EntryCanvas(self)

        self.__ui.splitter.replaceWidget(1, self.__ui.canvas)

        self.__entry_type = FrequencyResponse
        self.__parser = GtlAfcExcelParser()
        self.__entries = EntryList[self.__entry_type]([], self.__entry_type)
        self.__entries.connect_entries_added_handler(
            self.__handle_entries_added)
        self.__entries.connnect_entries_removed_handler(
            self.__handle_entries_removed)

        self.__ui.entries.entry_toggled.connect(self.__handle_entry_toggled)

    def exit_app(self):
        QApplication.quit()

    # pylint: disable-next=too-many-locals
    def open_files(self):
        settings = QSettings()
        directory = settings.value("last_dir")
        filefilter = "Все файлы (*.*)"

        files = self.__select_files(directory, filefilter)
        if not files:
            return

        new_directory = dirname(files[0])
        if new_directory != directory:
            settings.setValue("last_dir", new_directory)

        entries = self.__parser.parse_files(files)
        self.__set_entries_for_display(entries)

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

        entries = self.__parser.parse_files(files)
        self.__set_entries_for_display(entries)

    def add_files(self):
        raise NotImplementedError()

    def add_folder(self):
        raise NotImplementedError()

    def __select_files(self, directory: str, filefilter: str) -> list[str]:
        caption = "Открыть файлы"
        files, _ = QFileDialog.getOpenFileNames(
            self, caption, directory, filefilter)
        return files

    def __set_entries_for_display(self, entries: list[Entry]) -> None:
        self.__entries.clear()
        self.__entries.extend(entries)
        self.__ui.entries.set_entries(entries)
        self.__ui.canvas.set_entries(entries, self.__entry_type.y_headers[0])

    def __handle_entry_toggled(self, entryname, checked):
        entry = self.__entries.get_by_name(entryname)
        if checked:
            self.__ui.canvas.show_entry(entry)
        else:
            self.__ui.canvas.hide_entry(entry)

    def __handle_entries_added(self, entries):
        pass

    def __handle_entries_removed(self, entries):
        pass
