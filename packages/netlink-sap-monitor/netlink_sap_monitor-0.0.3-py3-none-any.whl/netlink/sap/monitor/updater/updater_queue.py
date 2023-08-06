from collections import defaultdict
import datetime
from ..core import AgeBracket

VB_RETURN_CODE = {
    0: "processed",
    1: "v1_processed",
    12: "stopped_no_retry",
    19: "canceled",
    21: "error_external",
    200: "error_in_v2",
    201: "error_in_collection",
    242: "started",
    244: "prepared",
    245: "v2_processed",
    246: "started",
    252: "started",
    248: "to_delete",
    249: "started",
    250: "started",
    251: "to_delete",
    253: "auto_dia",
    254: "auto_sys",
    255: "initial",
}

VB_RETURN_CODE_ERROR = (12, 19, 21, 200, 201)


def updater_queue(rfc_connection):
    age_bracket = AgeBracket()
    system_now = rfc_connection.datetime_user_to_system(rfc_connection.datetime)
    for row in rfc_connection.select("VBHDR", "VBUSR", "VBREPORT", "VBTCODE", "VBRC", "VBDATE"):
        system_datetime = datetime.datetime.strptime(row.vbdate, "%Y%m%d%H%M%S")
        age = system_now - system_datetime
        age_bracket.add(age, row)

    data = defaultdict(  # age bracket
        lambda: defaultdict(  # user
            lambda: defaultdict(  # report
                lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))  # t-code  # is error
            )
        )
    )  # status

    for age in age_bracket:
        for row in age_bracket[age]:
            status = VB_RETURN_CODE.get(int(row.vbrc), "error")
            is_error = int(row.vbrc) in VB_RETURN_CODE_ERROR or int(row.vbrc) not in VB_RETURN_CODE
            data[age][row.vbusr][row.vbreport][row.vbtcode][is_error][status] += 1

    return data
