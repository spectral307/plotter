from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow
import sys


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("plotter")
    app.setOrganizationName("GTLab")
    app.setOrganizationDomain("gtlab.pro")

    main = MainWindow()
    main.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
