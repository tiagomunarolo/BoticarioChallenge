import time


def split_date(date):
    current_time = date.split('-')
    numbers = [int(x) for x in current_time]
    return numbers[0], numbers[1]


def get_current_year_and_month():
    date = time.strftime("%Y-%m-%d")
    year, month = split_date(date)
    return year, month
