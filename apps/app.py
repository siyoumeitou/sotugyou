from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from apps.config import config
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

GEMINI_API_URL = "https://generativeai.googleapis.com"
API_KEY = "AIzaSyAA-D_2yDQFgSK-fj1oY1hdVbVHg18xwQg"
gemini_pro = genai.GenerativeModel("gemini-pro")

#SQLAlchemyをインスタンス化する
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
#login_view属性に未ログイン時にリダイレクトするエンドポイントを指定する
login_manager.login_view = "auth.signup"
#login_message属性にログイン後に表示するメッセージを指定する
#ここでは何も表示しないよう空を指定する
login_manager.login_message = ""
#Flaskインスタンス
app = Flask(__name__)
app.secret_key = 'your_secret_key'



#create_app関数を作成する
def create_app(config_key):
    #Flaskインスタンスを作成
    app = Flask(__name__)
    app.config.from_object(config[config_key])
    #アプリのコンフィグ設定をする
    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:5432@localhost:5432/sample',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        #SQLをコンソールログに出力する設定
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    )

    csrf.init_app(app)

    #SQLAlchemyとアプリを連携する
    db.init_app(app)
    #Migrateとアプリを連携する
    Migrate(app,db)


    login_manager.init_app(app)
    
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud,url_prefix="/crud")
    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth,url_prefix="/auth")
    from apps.base import views as base_views
    app.register_blueprint(base_views.base,url_prefix="/base")

    from apps.project import views as project_views
    app.register_blueprint(project_views.project,url_prefix="/project")
    from apps.chat import views as chat_views
    app.register_blueprint(chat_views.chat,url_prefix="/chat")
    from apps.memo import views as memo_views
    app.register_blueprint(memo_views.memo,url_prefix="/memo")
    #from apps.mail_box import views as mail_box_views
    #app.register_blueprint(mail_box_views.mail_box,url_prefix="/mail_box")
    from apps.calendar import views as calendar_views
    app.register_blueprint(calendar_views.calendar,url_prefix="/calendar")

    return app


if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app)