from apps.memo.forms import CreateMemoForm,CreateFolderForm
from apps.app import db,app
from apps.crud.models import User,Friend
from apps.memo.models import Memo,Folder
from flask import Blueprint,render_template,redirect,url_for
from flask_login import current_user,login_user,login_required

memo = Blueprint(
    "memo",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@memo.route("/")
@login_required
def index():
    return render_template("memo/index.html")

@memo.route("/app")
@login_required
def app():
    return render_template("memo/app.html")

@memo.route("/list")
@login_required
def list():
    #メモを取得
    memos = db.session.query(Memo).filter(Memo.creater_id==current_user.id,Memo.folder_id==0).all()
    folders = db.session.query(Folder).filter(Folder.creater_id==current_user.id).all()
    return render_template("memo/list_memo.html",memos=memos,folders=folders)

@memo.route("/main_memo/<int:memo_id>",methods=["GET","POST"])
@login_required
def main_memo(memo_id):
    memo = db.session.query(Memo).filter(Memo.memo_id==memo_id).first()
    return render_template("memo/main_memo.html",memo=memo)

@memo.route("/main_folder/<int:folder_id>",methods=["GET","POST"])
@login_required
def main_folder(folder_id):
    folder = db.session.query(Folder).filter(Folder.folder_id==folder_id).first()
    return render_template("memo/main_folder.html",folder=folder)


@memo.route("/create_memo",methods=["GET","POST"])
@login_required
def create_memo():
    form = CreateMemoForm()
    folders = db.session.query(Folder).filter(Folder.creater_id==current_user.id).all()
    form.folder.choices += [(folder.folder_id, folder.name) for folder in folders]
    if form.validate_on_submit():
        new_memo = Memo(
            folder_id = form.folder.data,
            creater_id = current_user.id,
            title = form.title.data,
            memo = form.memo.data
        )
        db.session.add(new_memo)
        db.session.commit()
        return redirect(url_for("memo.app",memo_id=new_memo.memo_id))

    return render_template("memo/create_memo.html",form=form)

@memo.route("/create_folder",methods=["GET","POST"])
@login_required
def create_folder():
    form = CreateFolderForm()
    if form.validate_on_submit():
        new_folder = Folder(
            creater_id = current_user.id,
            name = form.name.data,
        )
        db.session.add(new_folder)
        db.session.commit()
        return redirect(url_for("memo.create_folder"))

    return render_template("memo/create_folder.html",form=form)

@memo.route("/delete_memo/<int:memo_id>",methods=["GET","POST"])
@login_required
def delete_memo(memo_id):
    delete_memo = db.session.query(Memo).filter(Memo.memo_id==memo_id).first()
    db.session.delete(delete_memo)
    db.session.commit()
    return redirect(url_for("memo.create_memo"))

@memo.route("/delete_folder/<int:folder_id>",methods=["GET","POST"])
@login_required
def delete_folder(folder_id):
    delete_folder = db.session.query(Folder).filter(Folder.folder_id==folder_id).first()
    db.session.delete(delete_folder)
    db.session.commit()
    return redirect(url_for("memo.create_folder"))
