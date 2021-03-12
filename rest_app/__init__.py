import atexit
from flask import Flask

from rest_app.shared import db, scheduler
from rest_app.views.shared import blueprint as views_blueprint
from rest_app.services import refresh_offers


def create_app(start_background_job=True, shutdown_scheduler=True, **kwargs) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.update(**kwargs)

    db.init_app(app)
    app.register_blueprint(views_blueprint)
    if start_background_job:
        scheduler.init_app(app)

    with app.app_context():
        db.create_all()
        refresh_offers.schedule_refresh()

    if start_background_job:
        scheduler.start()
        if shutdown_scheduler:
            atexit.register(scheduler.shutdown)

    return app
