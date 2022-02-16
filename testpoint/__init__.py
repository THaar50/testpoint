from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from secrets import token_urlsafe

db = SQLAlchemy()

# TODO DB_USERNAME = os.environ.get('TESTPOINT_DB_USERNAME')
# TODO DB_PASSWORD = os.environ.get('TESTPOINT_DB_PASSWORD')
# TODO DB_NAME = os.environ.get('TESTPOINT_DB_NAME')
# TODO DB_PORT = os.environ.get('TESTPOINT_DB_PORT')


def create_app() -> Flask:
    """Creates a Flask application setting its secret and linking it with the database"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = token_urlsafe(nbytes=256)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # TODO app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost:{
    #  DB_PORT}/{DB_NAME}' TODO db.init_app(app=app)

    from .views import views

    app.register_blueprint(views,  url_prefix='/')

    return app
