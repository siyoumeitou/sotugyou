from apps.app import db
from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_required

base = Blueprint(
    "base",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@base.route("/")
@login_required
def screen():
    return render_template("base/screen.html")

@base.route("/title")
@login_required
def title():
    return render_template("base/title.html")

@base.route("/system")
@login_required
def system():
    return render_template("base/system.html")

@base.route("/menu")
@login_required
def menu():
    return render_template("base/menu.html")

@base.route("/app")
@login_required
def app():
    return render_template("base/app.html")

@base.route("/change")
@login_required
def change():
    return render_template("base/test.html")

@base.route("/change2")
#@login_required
def change2():
    return render_template("base/test2.html")