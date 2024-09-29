import datetime
from typing import List

import pytest
import pytz

from ovhsaver.__main__ import time_to_open

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
        ) for day in list_day
    ]


GENERATOR_MORNING = generate_mapping_date(hour=8, minute=0, second=0, list_day=LIST_WEEKDAY)

GENERATOR_EVENING = generate_mapping_date(hour=18, minute=59, second=59, list_day=LIST_WEEKDAY)

GENERATOR_TOO_EARLY = generate_mapping_date(hour=7, minute=59, second=59, list_day=LIST_WEEKDAY)

GENERATOR_TOO_LATE = generate_mapping_date(hour=19, minute=0, second=0, list_day=LIST_WEEKDAY)


@pytest.mark.parametrize("date", GENERATOR_MORNING)
def test_time_to_open_morning(date: datetime.datetime):
    """Test if time_to_open return True when it's morning"""
    assert time_to_open(date=date), "Should be online time (it's morning, after opening)"


@pytest.mark.parametrize("date", GENERATOR_EVENING)
def test_time_to_open_evening(date: datetime.datetime):
    """Test if time_to_open return True when it's evening"""
    assert time_to_open(date=date), "Should be online time (it's evening, before closing)"


@pytest.mark.parametrize("date", GENERATOR_TOO_EARLY)
def test_time_to_open_too_early(date: datetime.datetime):
    """Test if time_to_open return False when it's too early"""
    assert not time_to_open(date=date), "Should be offline time (it's too early to open)"


@pytest.mark.parametrize("date", GENERATOR_TOO_LATE)
def test_time_to_open_too_late(date: datetime.datetime):
    """Test if time_to_open return False when it's too late"""
    assert not time_to_open(date=date), "Should be offline time (it's too late to stay open)"


@pytest.mark.parametrize("date", GENERATOR_MORNING)
def test_time_to_open_morning_weekend(date: datetime.datetime):
    """Test if time_to_open return False the morning when it's weekend"""
    # Update day to Saturday, the next to Sunday
    assert not time_to_open(date=date.replace(day=7)), "Should be offline time (it's weekend)"
    assert not time_to_open(date=date.replace(day=1)), "Should be offline time (it's weekend)"


@pytest.mark.parametrize("date", GENERATOR_EVENING)
def test_time_to_open_evening_weekend(date: datetime.datetime):
    """Test if time_to_open return False the evening when it's weekend"""
    # Update day to Saturday, the next to Sunday
    assert not time_to_open(date=date.replace(day=7)), "Should be offline time (it's weekend)"
    assert not time_to_open(date=date.replace(day=1)), "Should be offline time (it's weekend)"
