import datetime
from typing import List

import pytest
import pytz

from conftest import FakeServer, FakeConnection
from ovhsaver.cloud import time_to_open, handle_server

TIME_ZONE = pytz.timezone("Europe/Paris")
TODAY = datetime.datetime.now(tz=TIME_ZONE)

LIST_WEEKDAY = [2, 3, 4, 5, 6]  # Monday to Friday
LIST_WEEKEND = [1, 7]  # Saturday or Sunday


def generate_mapping_date(hour: int, minute: int, second: int, list_day: List[int]) -> List[datetime.datetime]:
    return [
        datetime.datetime(
            year=TODAY.year,
            month=TODAY.month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
        )
        for day in list_day
    ]


GENERATOR_MORNING = generate_mapping_date(hour=8, minute=0, second=0, list_day=LIST_WEEKDAY)

GENERATOR_EVENING = generate_mapping_date(hour=18, minute=59, second=59, list_day=LIST_WEEKDAY)

GENERATOR_TOO_EARLY = generate_mapping_date(hour=7, minute=59, second=59, list_day=LIST_WEEKDAY)

GENERATOR_TOO_LATE = generate_mapping_date(hour=19, minute=0, second=0, list_day=LIST_WEEKDAY)


@pytest.mark.parametrize(
    ["list_date", "expected", "message"],
    [
        (GENERATOR_MORNING, True, "Should be online time (it's morning, after opening)"),
        (GENERATOR_EVENING, True, "Should be online time (it's evening, before closing)"),
        (GENERATOR_TOO_EARLY, False, "Should be offline time (it's too early to open)"),
        (GENERATOR_TOO_LATE, False, "Should be offline time (it's too late to stay open)"),
    ],
)
def test_time_to_open(list_date: List[datetime.datetime], expected: bool, message: str):
    """Test if time_to_open return True when it's morning"""
    for date in list_date:
        assert time_to_open(date=date) == expected, message


@pytest.mark.parametrize("list_date", [GENERATOR_MORNING, GENERATOR_EVENING])
def test_time_to_open_weekend(list_date: List[datetime.datetime]):
    """Test if time_to_open return False the morning when it's weekend"""
    # Update day to Saturday, the next to Sunday
    for date in list_date:
        assert not time_to_open(date=date.replace(day=7)), "Should be online time (it's weekend)"
        assert not time_to_open(date=date.replace(day=1)), "Should be online time (it's weekend)"


@pytest.mark.parametrize(
    ("list_date", "status", "expected"),
    [
        (GENERATOR_MORNING, "SHUTOFF", "STARTED"),
        (GENERATOR_MORNING, "ACTIVE", "NOTHING"),
        (GENERATOR_EVENING, "SHUTOFF", "STARTED"),
        (GENERATOR_EVENING, "ACTIVE", "NOTHING"),
        (GENERATOR_TOO_EARLY, "SHUTOFF", "NOTHING"),
        (GENERATOR_TOO_EARLY, "ACTIVE", "STOPPED"),
        (GENERATOR_TOO_LATE, "SHUTOFF", "NOTHING"),
        (GENERATOR_TOO_LATE, "ACTIVE", "STOPPED"),
    ],
)
def test_handler_server(list_date: List[datetime.datetime], status: str, expected: str):
    """Test if time_to_open return False the morning when it's weekend"""
    conn = FakeConnection()
    server = FakeServer(id=1, status=status)

    for date in list_date:
        result = handle_server(server=server, conn=conn, today=date)  # noqa
        assert result == expected, f"Should have '{expected}' the server"
