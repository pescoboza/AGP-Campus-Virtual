import time

from .models import User


###################################################
# Non-view helpers for report generation
###################################################
# CSV lines formatting
REPORT_HEADER = "gender, occupation, registered_on, birth_date, tstc_is_passed, tstc_passed_on, crvu_is_passed, crvu_passed_on, plmn_is_passed, plmn_passed_on, psta_is_passed, psta_passed_on, mama_is_passed, mama_passed_on, diag_is_passed, diag_passed_on\n"
REPORT_LINE_TEMPLATE = "{gender}, {occupation}, {registered_on}, {birth_date}, {tstc_is_passed}, {tstc_passed_on}, {crvu_is_passed}, {crvu_passed_on}, {plmn_is_passed}, {plmn_passed_on}, {psta_is_passed}, {psta_passed_on}, {mama_is_passed}, {mama_passed_on}, {diag_is_passed}, {diag_passed_on}\n"


def format_user(user):
    """Returns formatted line with user data."""

    return REPORT_LINE_TEMPLATE.format(
        gender=user.gender,
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
    out_filename = "temp/{}{}.csv".format(filename_base,
                                          str(time.time()).replace('.', ''))

    # Generate temporary CSV file
    try:
        with open(out_filename, 'w', encoding="utf-8") as ofile:
            ofile.write(REPORT_HEADER)
            for user in User.objects:
                line = format_user(user)
                ofile.write(line)

    except Exception as e:
        print("[ERROR] {}".format(e))
        raise e

    return out_filename
