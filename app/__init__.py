
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from config import config

db = SQLAlchemy()
ma = Marshmallow()
swag = Swagger()


def create_app(config_name):
    app = Flask(__name__)
    app.logger.debug('config_name=' + config_name)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .models import db  # force models to be imported
    db.init_app(app)
    ma.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api.calls import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .api.apispec import spec, definitions, paths
    from flasgger.utils import apispec_to_template
    swag.template = apispec_to_template(
        app=app,
        spec=spec,
        definitions=definitions,
        paths=paths
    )
    swag.init_app(app)

    return app
