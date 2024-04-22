from PyQt5 import uic, QtWidgets


class NewTaskDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NewTaskDialog, self).__init__(parent)
        uic.loadUi("ui/NewTask.ui", self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        super(NewTaskDialog, self).accept()

    def reject(self):
        super(NewTaskDialog, self).reject()
