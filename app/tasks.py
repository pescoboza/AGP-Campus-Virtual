from datetime import datetime, timedelta

from .import drive
from .google_drive import update_google_sheets_report


TASKS = {
    "update_google_sheets_report": {
        "func": lambda : update_google_sheets_report(drive),
        "trigger": "interval",
        "hours": 24,
        "name": "update_google_sheets_report",
        "id": "1",
        
        # Today at 11:00 pm
        "next_run_time": datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=0)

    },
    # "test_google_sheets_report": {
    #     "func": lambda : update_google_sheets_report(drive),
    #     "trigger": "interval",
    #     "minutes": 5,
    #     "name": "test_google_sheets_report",
    #     "id": "888",        
    #     "next_run_time": datetime.now() + timedelta(seconds=10)
    # }
}
