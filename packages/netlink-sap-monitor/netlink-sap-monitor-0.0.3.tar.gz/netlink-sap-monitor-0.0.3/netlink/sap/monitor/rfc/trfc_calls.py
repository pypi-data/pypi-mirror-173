from collections import defaultdict
import datetime
from ..core import AgeBracket


def transactional_rfc_calls(rfc_connection):
    age_bracket = AgeBracket()
    system_now = rfc_connection.datetime_user_to_system(rfc_connection.datetime)
    for row in rfc_connection.select(
        "ARFCSSTATE", "ARFCDEST", "ARFCSTATE", "ARFCFNAM", "ARFCUZEIT", "ARFCDATUM", "ARFCUSER", "ARFCTCODE"
    ):
        system_datetime = datetime.datetime.combine(
            datetime.datetime.strptime(row.arfcdatum, "%Y%m%d").date(),
            datetime.datetime.strptime(row.arfcuzeit, "%H%M%S").time(),
        )
        age = system_now - system_datetime
        age_bracket.add(age, row)

    data = defaultdict(  # age bracket
        lambda: defaultdict(  # destination
            lambda: defaultdict(  # state
                lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))  # function module  # user
            )
        )
    )  # t-code

    for age in age_bracket:
        for row in age_bracket[age]:
            data[age][row.arfcdest][row.arfcstate][row.arfcfnam][row.arfcuser][row.arfctcode] += 1

    return data
