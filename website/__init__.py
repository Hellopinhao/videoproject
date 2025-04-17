from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = "feedback.db"
DB2_NAME = "track.db"
DB3_NAME = "login.db"
DB4_NAME = "preferences.db"
DB5_NAME = "collection.db"
DB6_NAME = "personalInfo.db"
DB7_NAME = "browse.db"
DB8_NAME = "ratings.db"
DB9_NAME = 'browsingTime.db'
DB10_NAME = 'watch.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {DB2_NAME: f'sqlite:///{DB2_NAME}',
                                      DB3_NAME: f'sqlite:///{DB3_NAME}',
                                      DB4_NAME: f'sqlite:///{DB4_NAME}',
                                      DB5_NAME: f'sqlite:///{DB5_NAME}',
                                      DB6_NAME: f'sqlite:///{DB6_NAME}',
                                      DB7_NAME: f'sqlite:///{DB7_NAME}',
                                      DB8_NAME: f'sqlite:///{DB8_NAME}',
                                      DB9_NAME: f'sqlite:///{DB9_NAME}',
                                      DB10_NAME: f'sqlite:///{DB10_NAME}',
                                      }
    db.init_app(app)
    from .views import views
    from .auth import auth
    from .models import note
    from .models import activity
    from .models import user
    from .models import collection
    from .models import information
    from .models import browse
    from .models import rating
    from .models import watch
    create_database(app)
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.intro'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return user.query.get(int(id))
    return app

def create_database(app):
    if not (path.exists('website/' + DB_NAME) and path.exists('website/' + DB2_NAME) \
            and path.exists('website/' + DB3_NAME) and path.exists('website/' + DB4_NAME) \
            and path.exists('website/' + DB5_NAME) and path.exists('website/' + DB6_NAME) \
            and path.exists('website/' + DB7_NAME) and path.exists('website/' + DB8_NAME) \
            and path.exists('website/' + DB9_NAME) and path.exists('website/' + DB10_NAME)) :
        with app.app_context():
            db.create_all()
        print('Created Database!')
    return app