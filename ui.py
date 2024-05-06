from PyQt5 import uic, QtWidgets, Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

from new_task import NewTaskDialog, EditTaskDialog
from settings import SettingsWindow
import data_db
import run_copy


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.dialog_setting = None
        self.setWindowTitle("PG_backupper")
        self.setWindowIcon(QIcon("icon.png"))
        self.db = data_db.DataDB()
        self.task_buffer = list()
        self.refresh_list()
        self.refresh_buffer()
        self.refresh_future_task()
        self.statusBar().showMessage('Ожидание...')
        self.resize(910, 360)
        self.setFixedSize(910, 360)

        # Многопоточность
        self.CopyTask = run_copy.RunCopy()
        self.CopyTask.finished.connect(self.on_finished)

        # Назначаем действия кнопкам
        self.CreateTaskButton.clicked.connect(self.create_task)
        self.DeleteTaskButton.clicked.connect(self.delete_task)
        self.HideDeactivCheckBox.clicked.connect(self.refresh_list)
        self.ActiveTaskButton.clicked.connect(self.activate_task)
        self.DeactivTaskButton.clicked.connect(self.deactivate_task)
        self.TaskTable.doubleClicked.connect(self.edit_task)
        self.EditTaskButton.clicked.connect(self.edit_task)
        self.StartTaskButton.clicked.connect(self.start_task_button)
        self.ResizeButton.clicked.connect(self.resize_window)

        # Назначаем действия пунктам меню
        menu_file = self.menuBar().findChild(QMenu, "menu")
        settings_action = QAction("Настройки...", self)
        menu_file.addAction(settings_action)
        quit_action = QAction("Выход", self)
        menu_file.addAction(quit_action)
        quit_action.triggered.connect(self.close)
        settings_action.triggered.connect(self.program_settings)

        # Таймер для проверки задач и начала копирования
        self.timer = QTimer()
        self.timer.setInterval(60000)  # 60000 миллисекунд = 1 минута
        self.timer.timeout.connect(self.check_task)
        self.timer.timeout.connect(self.start_task)
        self.timer.start()

        # Сворачиваем в трей
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon("icon.png"))
        self.trayIcon.setToolTip("PG_backupper")
        self.trayMenu = QMenu()
        self.showAction = QAction("Показать")
        self.showAction.triggered.connect(self.show)
        self.quitAction = QAction("Выход")
        self.quitAction.triggered.connect(self.close)
        self.trayMenu.addAction(self.showAction)
        self.trayMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.show()

        result = self.db.get_settings()
        if result[2] == 1:
            self.program_settings()

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
                    self.refresh_future_task()

    def create_task(self):
        dialog_new_task = NewTaskDialog(self.db)
        dialog_new_task.exec_()
        self.refresh_list()
        self.refresh_future_task()

    def program_settings(self):
        self.dialog_setting = SettingsWindow(self.db)
        self.dialog_setting.exec_()

    def edit_task(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            id_task = self.TaskTable.item(row, 0).text()
            dialog_edit_task = EditTaskDialog(self.db, id_task)
            dialog_edit_task.exec_()
            self.refresh_list()
            self.refresh_future_task()

    def activate_task(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            id_task = self.TaskTable.item(row, 0).text()
            self.db.activate_task(id_task)
            self.refresh_list()
            self.refresh_future_task()

    def deactivate_task(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            id_task = self.TaskTable.item(row, 0).text()
            self.db.deactivate_task(id_task)
            self.refresh_list()
            self.refresh_future_task()

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
        self.TaskTable.setColumnHidden(2, True)
        self.TaskTable.setColumnHidden(5, True)

        self.TaskTable.setRowCount(0)
        task_list = self.db.get_list_of_tasks(self.HideDeactivCheckBox.isChecked())
        for task in task_list:
            row = self.TaskTable.rowCount()
            self.TaskTable.insertRow(row)
            self.TaskTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task[0])))
            self.TaskTable.setItem(row, 1, QtWidgets.QTableWidgetItem(task[1]))
            self.TaskTable.setItem(row, 2, QtWidgets.QTableWidgetItem(task[2]))
            self.TaskTable.setItem(row, 3, QtWidgets.QTableWidgetItem(task[3]))
            self.TaskTable.setItem(row, 4, QtWidgets.QTableWidgetItem(task[4]))
            self.TaskTable.setItem(row, 5, QtWidgets.QTableWidgetItem(task[5]))

    def refresh_buffer(self):
        self.BufferTable.clear()
        self.BufferTable.setColumnCount(3)
        self.BufferTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.BufferTable.setHorizontalHeaderLabels(['ID задачи', 'ID расписания', 'Статус'])
        self.BufferTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.BufferTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.BufferTable.setAlternatingRowColors(True)
        self.BufferTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.BufferTable.setShowGrid(True)
        self.BufferTable.setSortingEnabled(False)

        self.BufferTable.setRowCount(0)
        for task in self.task_buffer:
            row = self.BufferTable.rowCount()
            self.BufferTable.insertRow(row)
            self.BufferTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(task['id_task'])))
            self.BufferTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(task['id_schedule'])))
            self.BufferTable.setItem(row, 2, QtWidgets.QTableWidgetItem(task['status']))
        self.TaskFutureTable.resizeRowsToContents()

    def start_task_button(self):
        if self.check_selected_task():
            row = self.TaskTable.currentRow()
            id_task = self.TaskTable.item(row, 0).text()
            command = self.TaskTable.item(row, 5).text()
            task_name = self.TaskTable.item(row, 1).text()
            id_schedule = None
            self.statusBar().showMessage('Идет архивирование (Задача ' + task_name + ')')

            self.CopyTask.set_params(id_task, command, id_schedule)
            self.CopyTask.start()

    def check_task(self):
        result = self.db.get_schedule()
        if result is None:
            return
        for new_field in result:
            for field in self.task_buffer:
                if field['id_schedule'] == new_field[0] and field['id_task'] == new_field[1]:
                    break
            else:
                temp_dict = dict()
                temp_dict['id_schedule'] = new_field[0]
                temp_dict['id_task'] = new_field[1]
                temp_dict['status'] = 'Ожидает'
                temp_dict['name'] = new_field[2]
                self.task_buffer.append(temp_dict)

        for task in self.task_buffer:
            if task['status'] == 'Завершено':
                self.task_buffer.remove(task)
        self.refresh_buffer()
        self.refresh_future_task()

    def start_task(self):
        task = next((task for task in self.task_buffer if task['status'] == 'Ожидает'), None)
        if not task:
            return
        id_task = task['id_task']
        id_schedule = task['id_schedule']
        task_name = task['name']
        command = self.db.get_command(id_task)

        self.CopyTask.set_params(id_task, command[0], id_schedule)
        self.CopyTask.start()
        self.statusBar().showMessage('Идет архивирование (Задача ' + task_name + ')')

        for task in self.task_buffer:
            if task['id_task'] == id_task and task['id_schedule'] == id_schedule:
                task['status'] = 'Выполняется'
        self.refresh_buffer()

        self.db.update_schedule_status(id_schedule, 'Выполняется', '', '')

    def on_finished(self, param_dict):
        if param_dict['id_schedule'] is None:
            pass  # TODO: надо обозначить внеплановую копию
        else:
            self.db.update_schedule_status(param_dict['id_schedule'], 'Завершено',
                                           param_dict['start_time'], param_dict['end_time'])
            for task in self.task_buffer:
                if task['id_task'] == param_dict['id_task'] and task['id_schedule'] == param_dict['id_schedule']:
                    task['status'] = 'Завершено'
        self.refresh_buffer()
        self.refresh_future_task()
        self.statusBar().showMessage('Ожидание...')

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

    def resize_window(self):
        if self.ResizeButton.text() == "<-":
            self.resize(910, 360)
            self.setFixedSize(910, 360)
            self.ResizeButton.setText("->")
        else:
            self.resize(1380, 360)
            self.setFixedSize(1380, 360)
            self.ResizeButton.setText("<-")

    def refresh_future_task(self):
        self.TaskFutureTable.clear()
        self.TaskFutureTable.setColumnCount(3)
        self.TaskFutureTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.TaskFutureTable.setHorizontalHeaderLabels(['Наименование', 'Дата', 'Время'])
        self.TaskFutureTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TaskFutureTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TaskFutureTable.setAlternatingRowColors(True)
        self.TaskFutureTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.TaskFutureTable.setShowGrid(True)
        self.TaskFutureTable.setSortingEnabled(False)

        self.TaskFutureTable.setRowCount(0)
        result = self.db.get_future_tasks()
        for task in result:
            row = self.TaskFutureTable.rowCount()
            self.TaskFutureTable.insertRow(row)
            self.TaskFutureTable.setItem(row, 0, QtWidgets.QTableWidgetItem(task[4]))
            self.TaskFutureTable.setItem(row, 1, QtWidgets.QTableWidgetItem(
                            self.attache_zero(task[2])+':' + self.attache_zero(task[1])+':'+str(task[0])))
            self.TaskFutureTable.setItem(row, 2, QtWidgets.QTableWidgetItem(str(task[3])))
        self.TaskFutureTable.resizeRowsToContents()

    def closeEvent(self, event):
        if self.sender() is not None:
            self.close()
        else:
            self.hide()
            event.ignore()

    def showEvent(self, event):
        return super().showEvent(event)

    @staticmethod
    def attache_zero(param):
        if param < 10:
            return '0' + str(param)
        else:
            return str(param)
