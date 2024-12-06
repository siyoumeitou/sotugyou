from apps.app import db

class Schedule(db.Model):
    __tablename__ = "schedules"
    schedule_id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String)
    memo = db.Column(db.String)
    link = db.Column(db.String)
    date = db.Column(db.Date)
    color = db.Column(db.String)