import random
import string
from datetime import datetime, timedelta

from fastapi.testclient import TestClient


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_date():
    today = datetime.now()
    delta = datetime(today.year - 18, today.month, today.day) - datetime(today.year - 50, 1, 1)
    random_days = random.randint(0, delta.days)
    return datetime(today.year - 50, 1, 1) + timedelta(days=random_days)