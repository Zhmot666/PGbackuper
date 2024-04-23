import sys
from ui import QtWidgets, MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
