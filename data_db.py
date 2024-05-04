import datetime
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
    __GET_TASK_PARAMETERS = open('SQLScripts/get_task_parameters.txt').read()
    __EDIT_TASK = open('SQLScripts/edit_task.txt').read()
    __EDIT_TASK_PARAMETERS = open('SQLScripts/edit_task_parameters.txt').read()
    __INSERT_SCHEDULE = open('SQLScripts/insert_schedule.txt').read()
    __GET_SCHEDULE = open('SQLScripts/get_schedule.txt').read()
    __DELETE_SCHEDULE = open('SQLScripts/delete_schedule.txt').read()
    __EDIT_SCHEDULE_STATUS = open('SQLScripts/edit_schedule_status.txt').read()
    __GET_COMMAND = open('SQLScripts/get_command.txt').read()
    __SET_SCHEDULE_TIME = open('SQLScripts/set_schedule_time.txt').read()

    def __init__(self):
        self.__cursor = self.__CONNECTION.cursor()
        self.__cursor.execute("PRAGMA cache_size = 0;")
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS1)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS2)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS3)
        self.__cursor.executescript(self.__CREATE_TABLE_SCRIPTS4)
        result = self.__cursor.execute(self.__GET_SETTINGS)
        if result.fetchone() is None:
            self.__cursor.execute(self.__CREATE_TABLE_SCRIPTS5)
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
                param['path'], param['task_cmd'], param['log']))
        return id_new_task

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
        active = 'Неактивно' if active_only else '_'
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_LIST_OF_TASKS, ('Удалено', active))
            return result.fetchall()

    def get_task_parameters(self, id_task):
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_TASK_PARAMETERS, (int(id_task),))
            return result.fetchone()

    def get_schedule(self):
        current_data = datetime.datetime.now()
        year = current_data.year
        month = current_data.month
        day = current_data.day
        time = current_data.strftime("%H:%M")
        with self.__CONNECTION as self.sql:
            # result = self.sql.execute(self.__GET_SCHEDULE, (year, month, day, time, 'Ожидает'))
            result = self.sql.execute('''SELECT Schedule.ID_schedule, Schedule.ID_Task, TaskList.Name_Task
            FROM Schedule
            JOIN TaskList ON Schedule.ID_Task = TaskList.ID
            WHERE Schedule.Year = ? 
            AND Schedule.Month = ? 
            AND Schedule.Day = ?
            AND Schedule.PlanTime = ? 
            AND Schedule.Status = ?
            AND TaskList.Active = "Активно"
            AND TaskList.Deleted <> "Удалено"''', (year, month, day, time, "Ожидает"))
        return result.fetchall()

    def get_settings(self):
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_SETTINGS)
        return result.fetchone()

    def set_settings(self, **settings):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__SET_SETTINGS, (settings['pg_path'],))
            return

    def edit_task_parameters(self, **parameters_task):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__EDIT_TASK, (parameters_task['name'], int(parameters_task['id'])))
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__EDIT_TASK_PARAMETERS,
                             (parameters_task['database_name'], parameters_task['path'], parameters_task['prefix'],
                              parameters_task['server_address'], parameters_task['port'], parameters_task['time'],
                              str(parameters_task['type_backup']), parameters_task['login'],
                              parameters_task['task_cmd'], parameters_task['log'], parameters_task['id']))
        return

    def insert_schedule(self, *schedule_data):
        with self.__CONNECTION as self.sql:
            for schedule_field in schedule_data:
                self.sql.execute(self.__INSERT_SCHEDULE, (schedule_field['id_task'], schedule_field['year'],
                                                          schedule_field['month'], schedule_field['day'],
                                                          schedule_field['plan_time'], schedule_field['status'],))
        return

    def update_schedule_status(self, id_schedule, status, start_time, end_time):
        with self.__CONNECTION as self.sql:
            self.sql.execute(self.__EDIT_SCHEDULE_STATUS, (status, start_time, end_time, id_schedule))
        return

    def delete_schedule(self, id_task):
        with self.__CONNECTION as self.sql:
            # self.sql.execute(self.__DELETE_SCHEDULE, (id_task,))
            self.sql.execute('''DELETE FROM Schedule WHERE ID_Task = ? AND Status = "Ожидает"''', (id_task,))
        return

    def get_command(self, id_task):
        with self.__CONNECTION as self.sql:
            result = self.sql.execute(self.__GET_COMMAND, (id_task,))
        return result.fetchone()

    def set_time(self, id_schedule, time, start_stop):
        with self.__CONNECTION as self.sql:
            self.sql.execute("CALL UpdateScheduleTime(?, ?, ?)", (id_schedule, time, start_stop))
        return
