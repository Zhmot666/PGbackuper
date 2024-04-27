from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from NewTask import NewTaskDialog
from Settings import SettingsWindow
import data_db


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.dialog_setting = ''
        self.setWindowTitle("PG_backupper")
        self.setWindowIcon(QIcon("icon.png"))
        self.db = data_db.DataDB()
        self.refresh_list()

        # Назначаем действия кнопкам
        self.CreateTaskButton.clicked.connect(self.create_task)
        self.DeleteTaskButton.clicked.connect(self.delete_task)
        self.HideDeactivCheckBox.clicked.connect(self.refresh_list)
        self.ActiveTaskButton.clicked.connect(self.activate_task)
        self.DeactivTaskButton.clicked.connect(self.deactivate_task)
        self.TaskTable.doubleClicked.connect(self.edit_task)
        self.PushButtonSettings.clicked.connect(self.program_settings)

        # Таймер для проверки задач
        self.timer = QTimer()
        self.timer.setInterval(60000)  # 60000 milliseconds = 1 minute
        self.timer.timeout.connect(self.check_task)
        self.timer.start()

        # Сворачиваем в трей
        # self.setWindowIcon(QIcon("icon.png"))
        # self.trayIcon = QSystemTrayIcon(self)
        # self.trayIcon.setIcon(QIcon("icon.png"))
        # self.trayIcon.setToolTip("PG_backupper")
        # self.trayMenu = QMenu()
        # self.showAction = QAction("Show")
        # self.showAction.triggered.connect(self.show)
        # self.quitAction = QAction("Quit")
        # self.quitAction.triggered.connect(self.close)
        # self.trayMenu.addAction(self.showAction)
        # self.trayMenu.addAction(self.quitAction)
        # self.trayIcon.setContextMenu(self.trayMenu)
        # self.trayIcon.show()
        # self.setAttribute(Qt.WA_QuitOnClose, False)

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
        dialog_new_task = NewTaskDialog(self.db)
        dialog_new_task.exec_()
        self.refresh_list()

    def program_settings(self):
        self.dialog_setting = SettingsWindow(self.db)
        self.dialog_setting.exec_()
        # self.refresh_list()

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

    def check_task(self):
        print('Работает!!!')

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

    def closeEvent(self, event):
        pass
        # sender = event.sender()
        # if sender == self.trayIcon:
        #     # Сворачиваем в трей
        #     self.trayIcon.hide()
        #     event.ignore()
        # else:
        #     # Закрываем программу
        #     self.trayIcon.hide()
        #     event.accept()
