from PyQt5 import uic, QtWidgets, QtGui
from NewTask import NewTaskDialog
import data_db


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.db = data_db.DataDB()
        self.refresh_list()

        self.CreateTaskButton.clicked.connect(self.create_task)
        self.DeleteTaskButton.clicked.connect(self.delete_task)
        self.HideDeactivCheckBox.clicked.connect(self.refresh_list)

    def showEvent(self, event):
        pass

    def delete_task(self):
        pass

    def create_task(self):
        dialog = NewTaskDialog(self)
        dialog.exec_()

    def closeEvent(self, event):
        pass

    def refresh_list(self):
        task_list = self.db.get_list_of_tasks(self.HideDeactivCheckBox.isChecked())
        self.TaskTable.clear()
        self.TaskTable.setColumnCount(5)
        self.TaskTable.horizontalHeader().setStretchLastSection(True)
        self.TaskTable.setHorizontalHeaderLabels(["ID", "Название задачи", "Активность", "Расписание",
                                                  "Командная строка"])
        self.TaskTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TaskTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TaskTable.setAlternatingRowColors(True)
        self.TaskTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.TaskTable.setShowGrid(True)
        self.TaskTable.setSortingEnabled(False)
        # self.TaskTable.setColumnHidden(0, True)

        self.TaskTable.setRowCount(0)
        for task in task_list:
            row = self.TaskTable.rowCount()
            self.TaskTable.setItem(row, 0, QtWidgets.QTableWidgetItem(task[0]))
            self.TaskTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task[1]))
            self.TaskTable.setItem(row, 2, QtWidgets.QTableWidgetItem(task[2]))
            self.TaskTable.insertRow(row)
            # TODO: не отображается ID. Почему?
            # TODO: покрасить таблицу
            item = QtWidgets.QTableWidgetItem()
            if task[2] == "Активно":
                item.setForeground(QtGui.QColor("green"))
            else:
                item.setForeground(QtGui.QColor("red"))
