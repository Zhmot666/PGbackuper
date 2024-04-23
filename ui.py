from PyQt5 import uic, QtWidgets
from NewTask import NewTaskDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)

        self.CreateTaskButton.clicked.connect(self.create_task)

    def create_task(self):
        dialog = NewTaskDialog(self)
        dialog.exec_()

    def closeEvent(self, event):
        pass
