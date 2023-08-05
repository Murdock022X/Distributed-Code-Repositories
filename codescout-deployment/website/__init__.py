from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import json
from pathlib import Path
import logging as lg
from os import environ
from pathlib import Path

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

lg.basicConfig(filename=str(Path(environ.get("CODE_SCOUT_HOME")) / Path('logs/flask.app.log')), level=lg.DEBUG, format='[%(asctime)s] %(levelname)s --> %(module)s - %(message)s')

def create_app():
    app = Flask(__name__)

    app.config['PROJECT_ROOT'] = Path(__file__).parent

    with open(str(app.config['PROJECT_ROOT'] / Path('app_config.json'))) as conf:
        config = json.load(conf)

        app.config['SECRET_KEY'] = config['SECRET_KEY']

        app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']

        app.config['SEARCH_PAGE_LEN'] = config["SEARCH_PAGE_LEN"]
        app.config['USER_PAGE_LEN'] = config["USER_PAGE_LEN"]

        app.config['ENCRYPTION_KEY'] = config["ENCRYPTION_KEY"]

    db.init_app(app=app)

    login_manager.init_app(app=app)

    from website.auth.routes import auth
    app.register_blueprint(auth)

    from website.main.routes import main
    app.register_blueprint(main)

    app.logger.info('Flask App Configured.')

    return app
