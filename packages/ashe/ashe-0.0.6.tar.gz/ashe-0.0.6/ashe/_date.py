from datetime import datetime, timedelta

from typing import List, Union


def today(date_type: str = "str") -> Union[str, datetime.date]:
    _today = datetime.today().date()
    if date_type == "str":
        _today = str(_today)
    return _today


def yesterday(date_type: str = "str") -> Union[str, datetime.date]:
    _yesterday = datetime.today().date() - timedelta(days=1)
    if date_type == "str":
        _yesterday = str(_yesterday)
    return _yesterday


def get_interval_days(start: str = None, end: str = None, interval: int = None, reverse: bool = False) -> List[str]:
    if start is not None and end is not None and interval is not None:
        raise ValueError("three parameters (start end interval) cannot be present at the same time!")
    elif start is not None and end is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        interval = (end_date - start_date).days + 1
    elif start is not None and interval is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
    elif end is not None and interval is not None:
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        start_date = end_date - timedelta(days=interval-1)
    elif start is None and end is None and interval is not None:
        end_date = datetime.today().date()
        start_date = end_date - timedelta(days=interval - 1)
    else:
        raise ValueError("please check parameter, single parameter only support interval!")

    day_list = []
    for day_delta in range(interval):
        _day = start_date + timedelta(days=day_delta)
        day_list.append(_day.isoformat())

    if reverse:
        day_list.reverse()

    return day_list
