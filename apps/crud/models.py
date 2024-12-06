from datetime import datetime
from apps.app import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
# db.Modelを継承したUserクラスを作成する
class User(UserMixin,db.Model):
    #テーブル名を指定する
    __tablename__ = "users"
    #カラムを指定する
    id = db.Column(db.Integer,primary_key=True) #ID
    name = db.Column(db.String) #本名
    username = db.Column(db.String,unique=True) #表示する名前
    email = db.Column(db.String,unique=True,index=True) #Eメールのアドレス
    password_hash = db.Column(db.String) #パスワード
    if_ProjectLeader = db.Column(db.Boolean) #プロジェクトリーダーかどうか
    friends = db.relationship("Friend",backref="user",cascade="all, delete")
    created_at = db.Column(db.DateTime,default=datetime.now) #アカウント作成日時
    updated_at = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now) #最終ログイン

    #パスワードをセットするためのプロパティ
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    #パスワードをセットするためのセッター関数でハッシュ化したパスワードをセットする
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    #パスワードをチェックする
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    #メールアドレス重複をチェックする
    @staticmethod
    def is_duplicate_email(email):
        return User.query.filter_by(email=email).first() is not None
    
class Friend(db.Model):
    __tablename__ = "friends"
    friend_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    friend_user_id = db.Column(db.Integer)
    friend_name = db.Column(db.String)
    
    
#ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)