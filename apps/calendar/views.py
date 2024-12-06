from apps.app import db
from flask import Blueprint,render_template,redirect,url_for,jsonify
from flask_login import login_required,current_user
from apps.calendar.models import Schedule
from apps.calendar.forms import ScheduleForm
import json

calendar = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@calendar.route("/app")
@login_required
def app():
    return render_template("calendar/app.html")

@calendar.route("/app_calendar")
@login_required
def app_calendar():
    db_events = db.session.query(Schedule).filter(Schedule.user_id==current_user.id).all()
    events = []
    for event in db_events:
        events.append({
            "date": event.date.isoformat(),
            "title": event.title or "Untitled",
            "link": event.link or "#",
            "id": event.schedule_id,
            "color":event.color
        })
    print(events)
    return render_template("calendar/app_caleandar.html",events=events)

@calendar.route("/add_schedule",methods=["GET","POST"])
@login_required
def add_schedule():
    form = ScheduleForm()
    if form.validate_on_submit():
        new_schedule = Schedule(
            user_id = current_user.id,
            date = form.date.data,
            title = form.title.data,
            memo = form.memo.data,
            link = form.link.data,
            color = form.color.data
        )
        db.session.add(new_schedule)
        db.session.commit()
        return redirect(url_for("calendar.app_schedule",schedule_id=new_schedule.schedule_id))

    return render_template("calendar/add_schedule.html",form=form)

@calendar.route("/app_schedule/<int:schedule_id>",methods=["GET","POST"])
@login_required
def app_schedule(schedule_id):
    schedule = db.session.query(Schedule).filter(Schedule.schedule_id==schedule_id).first()
    return render_template("calendar/app_schedule.html",schedule=schedule)

@calendar.route("/dalete_schedule/<int:schedule_id>",methods=["GET","POST"])
@login_required
def delete_schedule(schedule_id):
    schedule = db.session.query(Schedule).filter(Schedule.schedule_id==schedule_id).first()
    db.session.delete(schedule)
    db.session.commit()
    return redirect(url_for("calendar.app_calendar"))