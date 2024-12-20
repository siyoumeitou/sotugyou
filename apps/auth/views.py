from apps.app import db
from apps.auth.forms import SignUpForm,LoginForm
from apps.crud.models import User
from flask import Blueprint,render_template,flash,url_for,redirect,request
from flask_login import login_user,logout_user

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@auth.route("/")
def index():
    return render_template("auth/index.html")

@auth.route("/signup",methods=["GET","POST"])
def signup():
    #SighUpFormをインスタンス化する
    form = SignUpForm()
    if form.validate_on_submit():

        #メールアドレス重複チェックをする
        if User.is_duplicate_email(form.email.data):
            flash("指定のメールアドレスは登録済みです")
            return redirect(url_for("auth.signup"))
        
        user = User(
            name=form.name.data,
            username=form.username.data,
            if_ProjectLeader=form.if_ProjectLeader.data,
            email=form.email.data,
            password=form.password.data,
        )
        
        #ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()
        #ユーザー情報をセッションに格納する
        login_user(user)
        #GETパラメータにnextキーが存在し、値がない場合はユーザーの一覧ページへリダイレクトする
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("base.screen")
        return redirect(next_)
    
    return render_template("auth/signup.html",form=form)

@auth.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("base.screen"))
        
        flash("ユーザー名かパスワードが不正です")
    return render_template("auth/login.html",form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))