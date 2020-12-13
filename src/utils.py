from uuid import uuid4
from datetime import datetime, timedelta


def generate_token():
    return f"{str(uuid4())}-{str(uuid4())}"


def future(**kwargs) -> datetime:
    return datetime.utcnow() + timedelta(**kwargs)
