from collections import defaultdict
import datetime
from ..core import AgeBracket


def lock_entries(rfc_connection):
    age_bracket = AgeBracket()
    system_now = rfc_connection.datetime_user_to_system(rfc_connection.datetime)
    for row in rfc_connection.enque_read(guname="").enq:
        system_datetime = datetime.datetime.combine(row.gtdate, row.gttime)
        age = system_now - system_datetime
        age_bracket.add(age, row)

    data = defaultdict(  # age bracket
        lambda: defaultdict(  # name
            lambda: defaultdict(  # mode
                lambda: defaultdict(  # object
                    lambda: defaultdict(  # client
                        lambda: defaultdict(  # user
                            lambda: defaultdict(lambda: 0)))))))  # tcode

    for age in age_bracket:
        for row in age_bracket[age]:
            data[age][row.gname][row.gmode][row.gobj][row.gclient][row.guname][row.gtcode] += 1

    return data
