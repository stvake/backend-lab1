from flask import Flask
from flask_migrate import Migrate
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.views import views
    app.register_blueprint(views)

    return app
