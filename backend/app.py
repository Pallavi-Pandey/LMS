from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from application.models import db, User, Role
from config import DevelopmentConfig
from application.resources import api
from application.sec import datastore
from application.worker import celery_init_app
import flask_excel as excel
from celery.schedules import crontab
from application.tasks import another_task, daily_reminder, revoke_access
from application.instances import cache
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    excel.init_excel(app)
    app.security = Security(app, datastore)
    cache.init_app(app)
    with app.app_context():
        import application.views

    return app


app = create_app()
CORS(app)
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):

    sender.add_periodic_task(
        # crontab(hour=16, minute=55, day_of_month=20),
        # for every 10 seconds
        crontab(minute="*/1"),
        daily_reminder.s('21f3003053@ds.study.iitm.ac.in',"aaaaaa"),
    )
    sender.add_periodic_task(
        # every hour
        crontab(minute=0, hour="*/1"),
        revoke_access.s(),  # Task to be executed
    )






if __name__ == '__main__':
    app.run(debug=True,port=5000)
