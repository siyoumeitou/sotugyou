from apps.crud.forms import UserForm
from apps.app import db,csrf,gemini_pro
from flask_sqlalchemy import SQLAlchemy
from apps.crud.models import User,Friend
from apps.project.models import Project,ProjectMember,Task,TasksProgresses,Check
from apps.project.forms import ProjectCreateForm,TaskCreateForm,TasksProgerssFrom
from flask import Blueprint,render_template,redirect, request,url_for
from flask_login import current_user,login_user,login_required
from sqlalchemy import func

project = Blueprint(
    "project",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@project.route("/")
@login_required
def index():
    return render_template("project/index.html")

@project.route("/app_project")
@login_required
def app_project():
    #自分が所属しているプロジェクトを１件だけ取得
    project = (
            db.session.query(Project)
            .join(ProjectMember, Project.project_id == ProjectMember.project_id)
            .filter(ProjectMember.member_id == current_user.id)
            .first()
        )
    return render_template("project/app_project.html",project=project)

@project.route("/list_project")
@login_required
def list_project():
    #自分が所属しているプロジェクトの取得
    projects = (
            db.session.query(Project)
            .join(ProjectMember, Project.project_id == ProjectMember.project_id)
            .filter(ProjectMember.member_id == current_user.id)
            .all()
        )
    return render_template("project/list_project.html",projects=projects)

@project.route("/main_project/<int:project_id>",methods=["GET","POST"])
@login_required
def main_project(project_id):
    return render_template("project/main_project.html",project_id=project_id)

@project.route("/select_project/<int:project_id>",methods=["GET","POST"])
@login_required
def select_project(project_id):
    project = db.session.query(Project).join(ProjectMember,ProjectMember.project_id==Project.project_id).filter(Project.project_id==project_id).first()
    return render_template("project/select_project.html",project=project)



#現在の全体の進捗割合を計算するフィルター
def calculate_average(project_id):
    average = (
    db.session.query(func.avg(TasksProgresses.percent))
    .join(Task,Task.task_id==TasksProgresses.task_id)
    .filter(Task.project_id == project_id)
    .scalar()
    )
    return average

project.add_app_template_filter(calculate_average, "average")

########################################################################

@project.route("/create_project",methods=["GET","POST"])
@login_required
def create_project():
    form = ProjectCreateForm()
    #現在のフレンドを取得
    friends = db.session.query(Friend).filter(Friend.user_id==current_user.id).all()
    #選択肢に入れる
    form.friends.choices = [(str(friend.friend_user_id), friend.friend_name) for friend in friends]

    if form.validate_on_submit():
        #プロジェクト新規作成
        project = Project(
            name = form.name.data,
            comment = form.comment.data,
            creater_id = current_user.id
        )
        db.session.add(project)
        db.session.flush()

        #メンバー登録
        #選択されたメンバーのIDを取得
        selected_members = form.friends.data
        #自分を入れる
        members = [{"id":current_user.id,"name":current_user.username}]
        #他のメンバーの情報をリストに格納する
        for member_id in selected_members:
            member = db.session.query(User).filter(User.id==member_id).first()
            members.append({"id":member_id,"name":member.username})
        #関数にデータを渡してメンバーを追加する
        add_new_project_member(project.project_id,members)
        return redirect(url_for("project.app_taspro",project_id=project.project_id))

    return render_template("project/create_project.html",form=form)

@project.route("/create_after/<int:project_id>",methods=["GET","POST"])
@login_required
def create_after(project_id):
    return render_template("project/create_after.html",project_id=project_id)

#プロジェクトメンバーを加える関数
def add_new_project_member(project_id,members):
    for member in members:
        new_member = ProjectMember(
            project_id = project_id,
            member_id = member["id"],
            member_name = member["name"]
        )
        db.session.add(new_member)
    db.session.commit()


#####################################################################
#####################################################################
#project_name
#####################################################################
#####################################################################
    


@project.route("/project_name/<int:project_id>/<int:task_id>",methods=["GET","POST"])
@login_required
def project_name(project_id,task_id):
    if task_id != 0:
        task = db.session.query(Task).filter(Task.task_id == task_id).first()
    else:
        task = None
    project = db.session.query(Project).filter(Project.project_id == project_id).first()
    return render_template("project/project_name.html",project=project,task=task)



#####################################################################
#####################################################################
#ここからタスク関係
#####################################################################
#####################################################################


@project.route("/app_task/<int:task_id>",methods=["GET","POST"])
@login_required
def app_task(task_id):
    task = db.session.query(Task).join(Project,Project.project_id == Task.project_id).filter(Task.task_id == task_id).first()
    return render_template("project/app_task.html",task=task)

@project.route("/app_taspro/<int:project_id>",methods=["GET","POST"])
@login_required
def app_taspro(project_id):
    return render_template("project/app_taspro.html",project_id=project_id)

@project.route("/main_task/<int:task_id>",methods=["GET","POST"])
@login_required
def main_task(task_id):
    #task_idからタスクを取得
    task = db.session.query(Task).join(Project,Project.project_id == Task.project_id).filter(Task.task_id == task_id).first()
    return render_template("project/main_task.html",project_id=task.project_id,task_id=task_id)

@project.route("/list_task/<int:project_id>",methods=["GET","POST"])
@login_required
def list_task(project_id):
    project = db.session.query(Project).filter(Project.project_id == project_id).first()
    #プロジェクトにリレーションしているタスクの取得
    tasks = project.tasks
    return render_template("project/list_task.html",project=project,tasks=tasks)

@project.route("/create_task/<int:project_id>",methods=["GET","POST"])
@login_required
def create_task(project_id):
    form = TaskCreateForm()
    if form.validate_on_submit():
        new_task = Task(
            project_id = project_id,
            name = form.name.data,
            description = form.description.data,
            comment = form.comment.data,
            creater_id = current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("project.app_task",task_id=new_task.task_id))

    return render_template("project/create_task.html",form=form,project_id=project_id)


@project.route("/select_task/<int:task_id>",methods=["GET","POST"])
@login_required
def select_task(task_id):
    task = Task.query.get(task_id)
    return render_template("project/select_task2.html",task=task,checked_count=checked_count)

#タスクごとのチェック数をカウントする関数
def checked_count(task_id):
    count = db.session.query(Check).filter(Check.task_id==task_id,Check.checked==True).count()
    print(count)
    return count



@project.route("/progress_registation/<int:task_id>",methods=["GET","POST"])
@login_required
def progress_registation(task_id):
    form = TasksProgerssFrom()
    if form.validate_on_submit():
        new_task_progress = TasksProgresses(
            task_id = task_id,
            register_id = current_user.id,
            register_name = current_user.username,
            name = form.name.data,
            progress = form.progress.data,
            comment = form.comment.data,
            percent = form.percent.data
        )
        db.session.add(new_task_progress)
        db.session.commit()
        return redirect(url_for("project.main_task",task_id=new_task_progress.task_id))

    return render_template("project/progress_registation.html",form=form,task_id=task_id)

#####################################################################
#####################################################################
#チェックボックス
#####################################################################
#####################################################################
@project.route("/select_check/<int:task_id>",methods=["GET","POST"])
@login_required
def select_check(task_id):
    task = Task.query.get(task_id)
    return render_template("project/select_check.html",task=task)


@project.route("/update_checkbox",methods=["GET","POST"])
def update_checkbox():
    data = request.get_json()
    check_id = data.get("id")
    is_checked = data.get("checked")

    check = Check.query.get(check_id)
    if check:
        check.checked = is_checked
        db.session.commit()
        print("更新成功")
    else:
        print("更新失敗")


@project.route("/update_sheet/<int:task_id>",methods=["GET","POST"])
def update_sheet(task_id):
    return redirect(url_for("select_task",task_id=task_id))

@project.route("/select_ai/<int:project_id>/<int:type>",methods=["GET","POST"])
def select_ai(project_id,type):
    project = Project.query.get(project_id)
    prompt = ""
    if type == 1:
        title = "タスクの優先順位"
        prompt = "以下のプロジェクトについて推奨されるタスクの実行する順番を教えてください。プロジェクト名:"+project.name+",今あるタスク名:"
        for task in project.tasks:
            prompt += task.name+","
        prompt += "1:タスク名 (以下理由を述べる文)<br> のように出力してください。最後にプロジェクト全体の進め方についての意見を述べてください。見やすさの為に改行を必ず使用してください。"
    elif type == 2:
        title = "タスクの提案"
        prompt = "以下のプロジェクトについて新たなタスクの提案をしてください(1~5個)。プロジェクト名:"+project.name+",タスク名:"
        for task in project.tasks:
            prompt += task.name+","
        prompt += "1:提案タスク名 (以下理由を述べる文)<br> のように出力し、見やすさの為に改行を必ず使用してください。"
    elif type == 3:
        title = "チェックリストの考案"
        prompt = "以下のタスクについてそれぞれチェックリストを考案してください。プロジェクト名:"+project.name+",タスク名:"
        for task in project.tasks:
            prompt += task.name+","
        prompt += "「1:タスク名<br><ul>~~</ul>」のように出力してください。"
    prompt += "HTMLを使って出力するので、改行や太文字にする場合はHTMLのタグを使って出力してください。(例:改行する<br>,**太文字**の代わりに<b>太文字</b>)"
    response = gemini_pro.generate_content(prompt)
    return render_template("project/select_ai.html",response=response.text,title=title)

