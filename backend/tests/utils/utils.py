import random
import secrets
import string
from datetime import datetime, timedelta


def random_lower_string() -> str:
    return "".join(secrets.choice(string.ascii_lowercase) for _ in range(16))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_birth_date():
    today = datetime.now()
    earliest_birth = datetime(today.year - 50, 1, 1)
    latest_birth = datetime(today.year - 18, today.month, today.day)
    delta = latest_birth - earliest_birth
    random_days = secrets.randbelow(delta.days + 1)
    random_date = earliest_birth + timedelta(days=random_days)
    return random_date.date()


if __name__ == '__main__':
    print(random_email())
    print(random_lower_string())
    print(random_birth_date())
    