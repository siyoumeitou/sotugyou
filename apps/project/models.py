from datetime import datetime
from apps.app import db

class Project(db.Model):
    __tablename__ = "projects"
    project_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    comment = db.Column(db.String)
    creater_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    project_member = db.relationship("ProjectMember",backref="project",cascade="all, delete")
    tasks = db.relationship("Task",backref="project",cascade="all, delete")
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class ProjectMember(db.Model):
    __tablename__ = "project_members"
    project_member_id = db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('projects.project_id'))
    member_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    member_name = db.Column(db.String)

class Task(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('projects.project_id'))
    name = db.Column(db.String)
    description = db.Column(db.String) #作業内容
    progresses = db.relationship("TasksProgresses",backref="task",cascade="all, delete") #進捗
    comment = db.Column(db.String) #詳細
    creater_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)


class TasksProgresses(db.Model):
    __tablename__ = "tasks_progresses"
    progress_id = db.Column(db.Integer,primary_key=True)
    task_id = db.Column(db.Integer,db.ForeignKey('tasks.task_id'))
    register_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    register_name = db.Column(db.String)
    name = db.Column(db.String)
    comment = db.Column(db.String)
    progress = db.Column(db.String)
    percent = db.Column(db.Integer)


class Check(db.Model):
    __tablename__ = "checks"
    check_id = db.Column(db.Integer,primary_key=True)
    task_id = db.Column(db.Integer,db.ForeignKey('tasks.task_id'))
    register_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    name = db.Column(db.String)
    comment = db.Column(db.String) #詳細
    checked = db.Column(db.Boolean)
