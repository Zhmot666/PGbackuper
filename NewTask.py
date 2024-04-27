from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog

import data_db


class TaskDialog(QtWidgets.QDialog):
    def __init__(self, db, id_task=None, parent=None):
        super(TaskDialog, self).__init__(parent)
        uic.loadUi("ui/NewTask.ui", self)
        self.id_task = id_task
        self.db = db
        self.init_ui()
        self.init_ui2()

    def init_ui(self):
        self.CancelButton.clicked.connect(self.cancel_button)
        self.SaveButton.clicked.connect(self.save_button)
        self.ChangePathButton.clicked.connect(self.changed_path)
        self.GeneratorButton.clicked.connect(self.generate_cmd)
        self.Task_id_hide.hide()

    def init_ui2(self):
        pass

    def save_button(self):
        if self.check_task():
            parameters_task = dict()
            parameters_task['id'] = self.Task_id_hide.text()
            parameters_task['name'] = self.NameTask.text()
            parameters_task['prefix'] = self.FilePrefix.text()
            parameters_task['time'] = self.TimeStart.text()
            parameters_task['server_address'] = self.ServerAddress.text()
            parameters_task['port'] = self.ServerPort.text()
            parameters_task['database_name'] = self.DataBaseName.text()
            parameters_task['login'] = self.UserName.text()
            if self.TextFile.isChecked():
                parameters_task['type_backup'] = 1
            elif self.Arhiv.isChecked():
                parameters_task['type_backup'] = 2
            elif self.Folder.isChecked():
                parameters_task['type_backup'] = 3
            elif self.TarArhiv.isChecked():
                parameters_task['type_backup'] = 4
            parameters_task['path'] = self.ChangedPath.text()
            self.save_button2(**parameters_task)

    def save_button2(self, **parameters_task):
        pass

    def generate_cmd(self):
        settings = self.db.get_settings()
        command_line = str(settings[1]) + '/pg_dump.exe'

        self.CmdTask.setText(command_line)

    def cancel_button(self):
        self.close()

    def check_task(self):
        # TODO: Проверить заполненность наименования
        # TODO: Проверить наименование на совпадение
        # TODO: Проверить заполненность адреса сервера
        # TODO: Проверить заполненность имени базы
        # TODO: Проверить заполненность порта
        # TODO: Проверить заполненность логина
        # TODO: Проверить заполненность типа архива
        # TODO: Проверить заполненность префикса имени файла
        # TODO: Проверить префикс на совпадение
        return True

    def changed_path(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.ChangedPath.setText(dirlist)


class NewTaskDialog(TaskDialog):

    def init_ui2(self):
        self.NameTask.setFocus()
        self.TextFile.setChecked(True)

    def save_button2(self, **parameters_task):
        self.db.add_new_task(**parameters_task)
        self.close()

class EditTaskDialog(TaskDialog):

    def init_ui2(self):
        self.Label_NewTask.setText('Редактировать задание')
        task_param = self.db.get_task_parameters(self.id_task)
        # for param in task_param:
        self.NameTask.setText(task_param[0])
        self.ServerAddress.setText(task_param[4])
        self.ServerPort.setText(task_param[5])
        self.DataBaseName.setText(task_param[6])
        self.UserName.setText(task_param[7])
        self.FilePrefix.setText(task_param[2])
        self.ChangedPath.setText(task_param[9])
        self.Task_id_hide.setText(str(task_param[1]))
        list_time = task_param[3].split(':')
        self.TimeStart.setTime(QTime(int(list_time[0]), int(list_time[1]), 0))

        if task_param[8] == 1:
            self.TextFile.setChecked(True)
        elif task_param[8] == 2:
            self.Arhiv.setChecked(True)
        elif task_param[8] == 3:
            self.Folder.setChecked(True)
        elif task_param[8] == 4:
            self.TarArhiv.setChecked(True)

        # 0 - Нименование +
        # 1 - ID +
        # 2 - префикс +
        # 3 - время +
        # 4 - сервер +
        # 5 - порт +
        # 6 - база +
        # 7 - юзер +
        # 8 - тип копии
        # 9 - путь +

    def save_button2(self, **parameters_task):
        self.db.edit_task_parameters(**parameters_task)
        self.close()
