import sqlite3


class DataDB:
    __CONNECTION = sqlite3.connect('db_backuper.db')
    __CREATE_TABLE_SCRIPTS1 = open('SQLScripts/create_TaskList.txt').read()
    __CREATE_TABLE_SCRIPTS2 = open('SQLScripts/create_TaskParameters.txt').read()
    __CREATE_TABLE_SCRIPTS3 = open('SQLScripts/create_Schedule.txt').read()
    __GET_LIST_OF_TASKS = open('SQLScripts/get_list_of_tasks.txt').read()


    def __init__(self):
        self.__cursor = self.__CONNECTION.cursor()
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS1)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS2)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS3)
        self.__CONNECTION.commit()

    def __del__(self):
        self.__cursor.close()
        self.__CONNECTION.close()

    def add_new_task(self):
        pass

    def activate_task(self):
        pass

    def deactivate_task(self):
        pass

    def delete_task(self):
        pass

    def get_list_of_tasks(self, active_only=True):
        active = 'Неактивно' if active_only else ''
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_LIST_OF_TASKS, (active,))
            return result.fetchall()

    def get_task_parameters(self):
        pass

    def get_schedule(self):
        pass
