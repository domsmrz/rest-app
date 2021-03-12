from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from functools import wraps
from typing import Callable

db = SQLAlchemy()
scheduler = APScheduler()


def add_scheduler_context(func: Callable) -> Callable:
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        with scheduler.app.app_context():
            func(*args, **kwargs)
    return wrapped_func


