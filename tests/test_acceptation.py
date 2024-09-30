import datetime
from typing import List

import pytest
import pytz

from conftest import FakeServer, FakeConnection
from ovhsaver.cloud import time_to_open, handle_server

TIME_ZONE = pytz.timezone("Europe/Paris")
TODAY = datetime.datetime.now(tz=TIME_ZONE)

LIST_WEEKDAY = [0, 1, 2, 3, 4]  # Monday to Friday
LIST_WEEKEND = [5, 6]  # Saturday or Sunday


def generate_mapping_date(hour: int, minute: int, second: int, list_day: List[int]) -> List[datetime.datetime]:
    result = []
    for day in list_day:
        if not (0 <= day <= 6):
            raise ValueError(f"List of day must contains id_weekday between 0-6 {list_day}")

        # Calculate the offset in days to get the next corresponding day.
        delta_days = (day - TODAY.weekday() + 7) % 7
        next_weekday = TODAY + datetime.timedelta(days=delta_days)

        # Generate date with specified hours, minutes and seconds
        result.append(
            datetime.datetime(
                year=next_weekday.year,
                month=next_weekday.month,
                day=next_weekday.day,
                hour=hour,
                minute=minute,
                second=second,
            )
        )
    return result


GENERATOR_MORNING = generate_mapping_date(hour=8, minute=0, second=0, list_day=LIST_WEEKDAY)

GENERATOR_EVENING = generate_mapping_date(hour=18, minute=59, second=59, list_day=LIST_WEEKDAY)

GENERATOR_TOO_EARLY = generate_mapping_date(hour=7, minute=59, second=59, list_day=LIST_WEEKDAY)

GENERATOR_TOO_LATE = generate_mapping_date(hour=19, minute=0, second=0, list_day=LIST_WEEKDAY)

GENERATOR_MORNING_WEEKEND = generate_mapping_date(hour=8, minute=0, second=0, list_day=LIST_WEEKEND)

GENERATOR_EVENING_WEEKEND = generate_mapping_date(hour=19, minute=0, second=0, list_day=LIST_WEEKEND)


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


@pytest.mark.parametrize("list_date", [GENERATOR_MORNING_WEEKEND, GENERATOR_EVENING_WEEKEND])
def test_time_to_open_weekend(list_date: List[datetime.datetime]):
    """Test if time_to_open return False the morning when it's weekend"""
    # Update day to Saturday, the next to Sunday
    for date in list_date:
        assert not time_to_open(date=date), "Should be online time (it's weekend)"


@pytest.mark.parametrize(
    ("list_date", "status", "expected"),
    [
        (GENERATOR_MORNING, "SHELVED", "STARTED"),
        (GENERATOR_MORNING, "ACTIVE", "NOTHING"),
        (GENERATOR_EVENING, "SHELVED", "STARTED"),
        (GENERATOR_EVENING, "ACTIVE", "NOTHING"),
        (GENERATOR_TOO_EARLY, "SHELVED", "NOTHING"),
        (GENERATOR_TOO_EARLY, "ACTIVE", "SHELVED"),
        (GENERATOR_TOO_LATE, "SHELVED", "NOTHING"),
        (GENERATOR_TOO_LATE, "ACTIVE", "SHELVED"),
    ],
)
def test_handler_server(list_date: List[datetime.datetime], status: str, expected: str):
    """Test if time_to_open return False the morning when it's weekend"""
    conn = FakeConnection()
    server = FakeServer(id=1, status=status)

    for date in list_date:
        result = handle_server(server=server, conn=conn, today=date)  # noqa
        assert result == expected, f"Should have '{expected}' the server"
