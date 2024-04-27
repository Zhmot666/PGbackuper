from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog

import data_db


class TaskDialog(QtWidgets.QDialog):
    def __init__(self, db, parent=None):
        super(TaskDialog, self).__init__(parent)
        uic.loadUi("ui/NewTask.ui", self)
        self.db = db
        self.init_ui()

        # Назначение кнопок
        self.CancelButton.clicked.connect(self.cancel_button)
        self.SaveButton.clicked.connect(self.save_button)
        self.ChangePathButton.clicked.connect(self.changed_path)

    def init_ui(self):
        pass

    def save_button(self):
        if self.check_task():
            parameters_task = dict()
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
            elif self.TarArhive.isChecked():
                parameters_task['type_backup'] = 4
            parameters_task['path'] = self.ChangedPath.text()

            self.db.add_new_task(**parameters_task)
            self.close()

    def generate_cmd(self):
        pass

    def cancel_button(self):
        # super(TaskDialog, self).reject()
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

    def get_task(self):
        pass

    def changed_path(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.ChangedPath.setText(dirlist)


class NewTaskDialog(TaskDialog):

    def init_ui(self):
        self.NameTask.setFocus()
        self.TextFile.setChecked(True)


class EditTaskDialog(TaskDialog):

    def get_task(self):
        pass
