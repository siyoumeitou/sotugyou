from datetime import datetime
from apps.app import db

class Folder(db.Model):
    __tablename__ = "folders"
    folder_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    creater_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    memo = db.relationship("Memo",backref="folders",cascade="all, delete")


class Memo(db.Model):
    __tablename__ = "memos"
    memo_id = db.Column(db.Integer,primary_key=True)
    folder_id = db.Column(db.Integer,db.ForeignKey('folders.folder_id'))
    creater_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    title = db.Column(db.String)
    memo = db.Column(db.String)
    updated_at = db.Column(db.DateTime,default=datetime.now)