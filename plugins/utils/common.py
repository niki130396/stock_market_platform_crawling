from datetime import datetime, date
from typing import List, Tuple


def parse_numeric_string(s: str) -> (int, float):
    if "," in s:
        s = s.replace(",", "")
    if "." in s:
        return float(s)
    return int(s)


def is_numeric_value(value: str):
    if not value[-1].isdigit():
        return False
    return True


def convert_to_normalized_quarter(d: datetime):
    if d.month <= 3:
        month = 3
    elif d.month <= 6:
        month = 6
    elif d.month <= 9:
        month = 9
    else:
        month = 12
    return datetime.strftime(date(d.year, month, 30), "%Y-%m-%d")


def remove_rows_prior_to_latest(rows: List[Tuple[int, int, datetime, float]], latest_date: datetime):
    if not latest_date:
        return rows
    for index, row in enumerate(rows):
        if row[2] <= latest_date:
            return rows[:index]
