import os
from datetime import datetime, timezone
import time

from config import current_config
from .models import User


###################################################
# Non-view helpers for report generation
###################################################
def years_since(begin, end=datetime.now(tz=timezone.utc)):
    """Helper function to get the integer number of years since a timestamp."""
    return int((end - begin).days / 365.25)

def date_to_datetime(date):
    return datetime(
        year=date.year,
        month=date.month,
        day=date.day
    )


# CSV lines formatting
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
REPORT_HEADER = "gender, age, occupation, registered_on, birth_date, tstc_is_passed, tstc_passed_on, crvu_is_passed, crvu_passed_on, plmn_is_passed, plmn_passed_on, psta_is_passed, psta_passed_on, mama_is_passed, mama_passed_on, diag_is_passed, diag_passed_on\n"
REPORT_LINE_TEMPLATE = "{gender}, {age}, {occupation}, {registered_on}, {birth_date}, {tstc_is_passed}, {tstc_passed_on}, {crvu_is_passed}, {crvu_passed_on}, {plmn_is_passed}, {plmn_passed_on}, {psta_is_passed}, {psta_passed_on}, {mama_is_passed}, {mama_passed_on}, {diag_is_passed}, {diag_passed_on}\n"


def format_user(user, now):
    """
    Returns formatted line with user data.
    
    :param datetime now: UTC aware datetime object for now
    :param user: User model object
    """
    dob_datetime = date_to_datetime(user.birth_date).replace(tzinfo=timezone.utc)
    age = years_since(dob_datetime, now)

    return REPORT_LINE_TEMPLATE.format(
        gender=user.gender,
        age=age,
        occupation=user.occupation,
        registered_on=user.registered_on,
        birth_date=user.birth_date,
        tstc_is_passed=int(user.quiz_data["tstc"]["is_passed"]),
        crvu_is_passed=int(user.quiz_data["crvu"]["is_passed"]),
        plmn_is_passed=int(user.quiz_data["plmn"]["is_passed"]),
        psta_is_passed=int(user.quiz_data["psta"]["is_passed"]),
        mama_is_passed=int(user.quiz_data["mama"]["is_passed"]),
        diag_is_passed=int(user.quiz_data["diag"]["is_passed"]),
        tstc_passed_on=user.quiz_data["tstc"]["passed_on"],
        crvu_passed_on=user.quiz_data["crvu"]["passed_on"],
        plmn_passed_on=user.quiz_data["plmn"]["passed_on"],
        psta_passed_on=user.quiz_data["psta"]["passed_on"],
        mama_passed_on=user.quiz_data["mama"]["passed_on"],
        diag_passed_on=user.quiz_data["diag"]["passed_on"]
    )


def generate_user_report(filename_base):
    """  
    Generates the csv user report.    
    :param str filename_base: Base name of the csv file.

    :return: Returns name of the file created.
    """

    # Dynamic filename linked to time
    out_filename = "{}{}.csv".format(filename_base, str(time.time()).replace('.', ''))
    out_path = os.path.join(current_config.TEMP_FOLDER, out_filename)
    utc_aware_now = datetime.now(tz=timezone.utc)

    # Generate temporary CSV file
    try:
        with open(out_path, 'w', encoding="utf-8") as ofile:
            ofile.write(REPORT_HEADER)
            for user in User.objects:
                line = format_user(user, utc_aware_now)
                ofile.write(line)

    except Exception as e:
        print("[ERROR] {}".format(e))
        raise e

    return out_path
