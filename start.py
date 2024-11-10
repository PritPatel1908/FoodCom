from pathlib import Path
import os
import time
from datetime import datetime
from pathlib import Path
from SMWinservice import SMWinservice
import subprocess

def startServer():
    subprocess.run(['python', 'manage.py', 'runserver'])

class PythonFoodComServiceStart(SMWinservice):
    _svc_name_ = "FoodComService"
    _svc_display_name_ = "Python FoodCom Service"
    _svc_description_ = "This Is A FoodComService RunServer Service"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        startServer()

if __name__ == '__main__':
    PythonFoodComServiceStart.parse_command_line()