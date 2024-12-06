from datetime import datetime
from apps.app import db

class Mail(db.Model):
    __tablename__ = "mail"
    mail_id = db.Column(db.Integer,primary_key=True)
    sender_id = db.Column(db.Integer,db.ForeignKey("users.id")) #送り主
    recipient_id = db.Column(db.Integer,db.ForeignKey("users.id")) #受取主
    subject = db.Column(db.String) #件名
    content = db.Column(db.String) #本文
    image = db.Column(db.String,nullable=True) #送付物
    readed = db.Column(db.Boolean) #読んだかどうか
    sended_at = db.Column(db.DateTime,default=datetime.now)