import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Creates database
dbase = SQLAlchemy()
DB_NAME = "database.dbase"


# Referenced Website: https://www.youtube.com/watch?v=dam0GPOAvVI
# Creates the Application Method
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'adsfladfjl'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    dbase.init_app(app)

    from .userview import views
    from .authentication import authentication

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(authentication, url_prefix='/')

    from .dbmodels import User

    create_database(app)

    login_mgr = LoginManager()
    login_mgr.login_view = 'authentication.login'
    login_mgr.init_app(app)

    @login_mgr.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# Creates database
def create_database(app):
    with app.app_context():
        dbase.drop_all()
        dbase.create_all()
        print('Created Database!')
