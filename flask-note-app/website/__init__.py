#will make website folder a python package
from flask import Flask
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jeonjungkook970901'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    create_database(app)

    login_manager = LoginManager()
    #where should flask redirect if user not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        #tells flask how we load a user
        #query.get works the same way as filter_by but by default it will look for the primary key
        return User.query.get(int(id))

    return app

#check if db already exists, and if not create it
def create_database(app):
    #using path to determine if there is a path to our db
    if not path.exists('website/' + DB_NAME):
        #we need to tell sqlalchemy which app we are creating the db fo
        db.create_all(app=app)
        print('Created Database!')