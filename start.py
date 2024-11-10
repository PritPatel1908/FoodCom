# django_service

import os
import sys
import win32serviceutil
import win32service
import win32event
from django.core.management import execute_from_command_line

class DjangoService(win32serviceutil.ServiceFramework):
    _svc_name_ = "DjangoService"
    _svc_display_name_ = "Django FoodCom Service"
    _svc_description_ = "A Windows service to run Django FoodCom Project server."

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        # Set the Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodCom.settings')

        # Run Django's development server on a specified IP and port
        execute_from_command_line([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])

        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DjangoService)