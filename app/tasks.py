from datetime import datetime, timedelta

from .import drive
from .google_drive import upload_csv_as_google_sheets


def update_google_sheets_report():


TASKS = {
    "update_google_sheets_report": {
        "func": lambda: print("[UPDATE GOOGLE SHEETS TASK] {} Updated Google sheets".format(
            datetime.now().time())),
        "trigger": "interval",
        "hours": 24,
        "name": "update_google_sheets_report",
        "id": "1",
        # Today at 11:00 pm
        "next_run_time": datetime.now().replace(
            hour=23, minute=0, second=0, microsecond=0)
    },
    "mock": {
        "func": lambda: print("[MOCK TASK] {} Hello, I am a mock task for testing".format(
            datetime.now().time())),
        "trigger": "interval",
        "seconds": 30,
        "name": "mock_task",
        "id": "333",
        # Late 5 min
        "next_run_time": datetime.now() - timedelta(minutes=5)
    }
}
