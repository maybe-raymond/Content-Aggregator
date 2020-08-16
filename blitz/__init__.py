from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from celery import Celery
from flask_mail import Mail



app  = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]='65446464566g6d4651c66s461c6v651v'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["MAIL_SERVER"]= "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"]= False
app.config["MAIL_USE_SSL"] = True


#
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail= Mail(app)

from blitz import routes
