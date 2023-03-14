import sys

from PySide6 import QtWidgets

from backup_manager_pyside.statics.styles.load_styles import load_styles

from backup_manager_pyside.views.main_window import MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    load_styles(app)
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
