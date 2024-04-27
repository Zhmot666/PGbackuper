from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import data_db


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, db):
        super(SettingsWindow, self).__init__()
        uic.loadUi("ui/Settings.ui", self)
        # self.db_settings = data_db.DataDB()
        self.db_settings = db
        self.init_ui()

        # Назначение кнопок
        self.ChangePGDumpPathButton.clicked.connect(self.change_pg_path)
        self.CancelButton.clicked.connect(self.cancel_button)
        self.SaveButton.clicked.connect(self.save_button)

    def init_ui(self):

        settings = self.db_settings.get_settings()
        self.PGDumpPath.setText(settings[1])

    def save_button(self):
        settings_dict = dict()
        settings_dict['pg_path'] = self.PGDumpPath.text()
        self.db_settings.set_settings(**settings_dict)
        self.close()

    def cancel_button(self):
        self.close()

    def change_pg_path(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        self.PGDumpPath.setText(dirlist)
