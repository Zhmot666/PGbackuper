import sys
from ui import QtWidgets, MainWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open('CSS/Style2.css').read())
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
