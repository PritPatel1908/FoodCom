from pathlib import Path
import os
import time
from datetime import datetime
from pathlib import Path
from SMWinservice import SMWinservice

def writeToFile():
    BASE_DIR = Path(__file__).resolve().parent.parent
    DIR = os.path.join(BASE_DIR,'log.txt')
    while True:
        with open(DIR, 'a+') as file:
            file.write(str(datetime.now()))

class PythonFoodComServiceStart(SMWinservice):
    _svc_name_ = "FoodComService"
    _svc_display_name_ = "Python FoodCom Service"
    _svc_description_ = "This Is A FoodComService RunServer Service"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        writeToFile()

if __name__ == '__main__':
    PythonFoodComServiceStart.parse_command_line()