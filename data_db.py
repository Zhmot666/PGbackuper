import sqlite3


class DataDB:
    __CONNECTION = sqlite3.connect('db_backuper.db')
    __CREATE_TABLE_SCRIPTS1 = open('SQLScripts/create_TaskList.txt').read()
    __CREATE_TABLE_SCRIPTS2 = open('SQLScripts/create_TaskParameters.txt').read()
    __CREATE_TABLE_SCRIPTS3 = open('SQLScripts/create_Schedule.txt').read()
    __CREATE_TABLE_SCRIPTS4 = open('SQLScripts/create_Settings.txt').read()
    __CREATE_TABLE_SCRIPTS5 = open('SQLScripts/create_Settings2.txt').read()
    __GET_LIST_OF_TASKS = open('SQLScripts/get_list_of_tasks.txt').read()
    __CREATE_TASKS = open('SQLScripts/create_tasks.txt').read()
    __CREATE_PARAMETERS = open('SQLScripts/create_parameters.txt').read()
    __DELETE_TASKS = open('SQLScripts/delete_tasks.txt').read()
    __ACTIVATE_TASKS = open('SQLScripts/activate_tasks.txt').read()
    __DEACTIVATE_TASKS = open('SQLScripts/deactivate_tasks.txt').read()
    __GET_SETTINGS = open('SQLScripts/get_settings.txt').read()
    __SET_SETTINGS = open('SQLScripts/set_settings.txt').read()

    def __init__(self):
        self.__cursor = self.__CONNECTION.cursor()
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS1)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS2)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS3)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS4)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS4)
        self.__CONNECTION.commit()

    def __del__(self):
        self.__cursor.close()
        self.__CONNECTION.close()

    def add_new_task(self, **param):
        with self.__CONNECTION as self.sql:
            id_new_task = self.sql.execute(self.__CREATE_TASKS, (param['name'], 'Активно', '+'))
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__CREATE_PARAMETERS, (
                id_new_task.lastrowid, param['prefix'], param['time'], param['server_address'],
                param['port'], param['database_name'], param['login'], param['type_backup'],
                param['path']))

    def activate_task(self, id_task):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__ACTIVATE_TASKS, ('Активно', id_task))

    def deactivate_task(self, id_task):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__DEACTIVATE_TASKS, ('Неактивно', id_task))

    def delete_task(self, id_task):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__DELETE_TASKS, ('Удалено', id_task))

    def get_list_of_tasks(self, active_only=True):
        active = 'Неактивно' if active_only else ''
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_LIST_OF_TASKS, ('Удалено', active))
            return result.fetchall()

    def get_task_parameters(self):
        pass

    def get_schedule(self):
        pass

    def get_settings(self):
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_SETTINGS)
            return result.fetchone()

    def set_settings(self, **settings):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__SET_SETTINGS, (settings['pg_path'],))
            return
