from PyQt5 import uic, QtWidgets
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
        self.ActiveTaskButton.clicked.connect(self.activate_task)
        self.DeactivTaskButton.clicked.connect(self.deactivate_task)
        self.TaskTable.doubleClicked.connect(self.edit_task)

    def delete_task(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            if row == -1:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Выберите в списке задачу для удаления')
                msg.setWindowTitle('Ошибка')
                msg.exec_()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Question)
                msg.setText('Вы действительно хотите удалить эту задачу?')
                msg.setWindowTitle('Подтверждение')
                msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
                msg.setEscapeButton(QtWidgets.QMessageBox.No)

                msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                retval = msg.exec_()
                if retval == QtWidgets.QMessageBox.Yes:
                    self.db.delete_task(self.TaskTable.item(row, 0).text())
                    self.refresh_list()

    def create_task(self):
        dialog = NewTaskDialog(self)
        dialog.exec_()

    def edit_task(self):
        pass

    def activate_task(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            id_task = self.TaskTable.item(row, 0).text()
            self.db.activate_task(id_task)
            self.refresh_list()

    def deactivate_task(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            id_task = self.TaskTable.item(row, 0).text()
            self.db.deactivate_task(id_task)
            self.refresh_list()

    def closeEvent(self, event):
        pass

    def refresh_list(self):

        self.TaskTable.clear()
        self.TaskTable.setColumnCount(6)
        self.TaskTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.TaskTable.horizontalHeader().setStretchLastSection(True)
        self.TaskTable.setHorizontalHeaderLabels(['ID', 'Название задачи', 'Статус', 'Удаление', 'Расписание',
                                                  'Командная строка'])
        self.TaskTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TaskTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TaskTable.setAlternatingRowColors(True)
        self.TaskTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.TaskTable.setShowGrid(True)
        self.TaskTable.setSortingEnabled(False)
        self.TaskTable.setColumnHidden(0, True)
        # self.TaskTable.setColumnHidden(3, True)
        # self.TaskTable.setColumnHidden(1, False)

        self.TaskTable.setRowCount(0)
        task_list = self.db.get_list_of_tasks(self.HideDeactivCheckBox.isChecked())
        for task in task_list:
            row = self.TaskTable.rowCount()
            self.TaskTable.insertRow(row)
            self.TaskTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task[0])))
            self.TaskTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task[1]))
            self.TaskTable.setItem(row, 2, QtWidgets.QTableWidgetItem(task[2]))
            self.TaskTable.setItem(row, 3, QtWidgets.QTableWidgetItem(task[3]))

        self.TaskTable.resizeColumnsToContents()
        self.TaskTable.resizeRowsToContents()

    def check_selected_task(self):
        row = self.TaskTable.currentRow()
        if row == -1:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Выберите задачу из списка")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return False
        else:
            return True
