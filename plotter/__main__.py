# Reason: PyQt6 is a third party module.
# pylint: disable-next=no-name-in-module
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow
import sys


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("plotter")
    app.setOrganizationName("GTLab")
    app.setOrganizationDomain("gtlab.pro")

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
