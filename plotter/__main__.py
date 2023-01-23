import sys
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtCore import QSettings
# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("plotter")
    app.setOrganizationName("GTLab")
    app.setOrganizationDomain("gtlab.pro")

    settings = QSettings()
    if not settings.value("default_dir"):
        settings.setValue("default_dir", "/")
    if not settings.value("previous_dir"):
        settings.setValue("previous_dir", settings.value("default_dir"))

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
