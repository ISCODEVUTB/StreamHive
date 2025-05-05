import secrets
import string
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from backend.core.config import settings


def random_lower_string() -> str:
    return "".join(secrets.choice(string.ascii_lowercase) for _ in range(16))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_birth_date() -> datetime:
    today = datetime.now()
    earliest_birth = datetime(today.year - 50, 1, 1)
    latest_birth = datetime(today.year - 18, today.month, today.day)
    delta = latest_birth - earliest_birth
    random_days = secrets.randbelow(delta.days + 1)
    random_date = earliest_birth + timedelta(days=random_days)
    return random_date.date()


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers