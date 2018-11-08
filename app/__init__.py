
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from config import config

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .models import db  # force models to be imported
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api.calls import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
