from datetime import datetime
from apps.app import db

class Chat(db.Model):
    __tablename__ = "chats"
    chat_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,primary_key=True) 
    type = db.Column(db.String) #個チャorグルチャ
    chat_name = db.Column(db.String) #チャット名(グループ用)
    created_at = db.Column(db.DateTime,default=datetime.now) #作成日時
    updated_at = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now) #更新日時
    member = db.relationship("ChatMember",backref="chat",cascade="all, delete")
    content = db.relationship("ChatContent",backref="chat",cascade="all, delete")
    #個人チャットの場合は自分のidと相手のidで2つChatができる
    #グループチャットの場合は1つの
    __table_args__ = (
        db.PrimaryKeyConstraint('chat_id', 'user_id'),  # 2つのカラムを主キーに指定
    )

class ChatContent(db.Model):
    __tablename__ = "chat_contents"
    content_id = db.Column(db.Integer,primary_key=True)
    chat_id = db.Column(db.Integer,db.ForeignKey('chats.chat_id'))
    sender_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    sender_name = db.Column(db.String)
    content = db.Column(db.String)
    image = db.Column(db.String,nullable=True)
    sended_at = db.Column(db.DateTime,default=datetime.now)

class ChatMember(db.Model):
    __tablename__ = "chat_members"
    chat_member_id = db.Column(db.Integer,primary_key=True)
    chat_id = db.Column(db.Integer,db.ForeignKey('chats.chat_id'))
    member_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    member_name = db.Column(db.String)