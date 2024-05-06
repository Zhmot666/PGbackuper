import subprocess
import datetime
from PyQt5.QtCore import QThread, pyqtSignal


class RunCopy(QThread):
    finished = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.param_dict = dict()
        self.id_task = None
        self.id_schedule = None
        self.command_line = None

    def set_params(self, id_task, command_line, id_schedule):
        self.id_task = id_task
        self.command_line = command_line
        self.id_schedule = id_schedule

    def run(self):
        current_datetime = datetime.datetime.now()
        day = current_datetime.day
        month = current_datetime.month
        year = current_datetime.year
        time = self.attache_zero(current_datetime.hour) + '-' + self.attache_zero(current_datetime.minute)

        correct_cmd = self.command_line.replace('[DT]', self.attache_zero(day) + '-' +
                                                self.attache_zero(month) + '-' + str(year) + '_' + time)
        if self.id_schedule is not None:
            self.param_dict['start_time'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        result = subprocess.run(correct_cmd, stderr=subprocess.PIPE, text=True)
        output = result.stderr
        if self.id_schedule is not None:
            self.param_dict['end_time'] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.param_dict['return_code'] = result.returncode
        self.param_dict['id_task'] = self.id_task
        self.param_dict['id_schedule'] = self.id_schedule
        self.param_dict['log'] = output
        self.finished.emit(self.param_dict)

    @staticmethod
    def attache_zero(param):
        if param < 10:
            return '0' + str(param)
        else:
            return str(param)
