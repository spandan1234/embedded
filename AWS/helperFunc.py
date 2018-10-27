from datetime import datetime


def strtoDate(date):
    ''':type date: str
    :rtype: status: datetime.timedelta'''
    date = [int(x) for x in date.split('-')]
    formatted_date = datetime.date(date[0], date[1], date[2])
    return formatted_date
