from apps.chat.forms import AddChatForm,ChatForm,CreateGroupChatForm
from apps.app import db,app
from apps.crud.models import User,Friend
from apps.chat.models import Chat,ChatMember,ChatContent
from flask import Blueprint,render_template,redirect,url_for
from flask_login import current_user,login_user,login_required
from flask_socketio import SocketIO,send

chat = Blueprint(
    "chat",
    __name__,
    template_folder="templates",
    static_folder="static",
)
socketio = SocketIO(app)

@chat.route("/")
@login_required
def index():
    return render_template("chat/index.html")

@chat.route("/app")
@login_required
def app():
    return render_template("chat/app.html")

@chat.route("/list")
@login_required
def list():
    #自分のチャット先を取得
    chats = (db.session.query(Chat)
            .join(ChatMember, Chat.chat_id == ChatMember.chat_id)
            .filter(ChatMember.member_id == current_user.id,Chat.user_id==current_user.id)
            .all()
            )
    groups = (db.session.query(Chat)
            .join(ChatMember,Chat.chat_id == ChatMember.chat_id)
            .filter(ChatMember.member_id == current_user.id,Chat.type == "Group")
    )
    return render_template("chat/list.html",chats=chats,groups=groups)

@chat.route("/main/<int:chat_id>",methods=["GET","POST"])
@login_required
def main_chat(chat_id):
    form = ChatForm()
    if form.validate_on_submit():
        chat_content = ChatContent(
            chat_id = chat_id,
            sender_id = current_user.id,
            sender_name = current_user.username,
            content = form.chat.data,
            image = None
        )
        db.session.add(chat_content)
        db.session.commit()
        return redirect(url_for("chat.main_chat",chat_id=chat_id))

    chats = db.session.query(ChatContent).filter(ChatContent.chat_id == chat_id).all()
    return render_template("chat/main.html",form=form,chats=chats,chat_id=chat_id)



@chat.route("/add_chat",methods=["GET","POST"])
@login_required
def add_chat():
    form = AddChatForm()
    if form.validate_on_submit():
        if current_user.username==form.username.data:
            print("自分は登録できないよ")
            return redirect(url_for("chat.add_chat"))
        search = db.session.query(User).filter(User.username==form.username.data).first()
        #ユーザーが存在しているか
        if search:
            #ユーザーが既にフレンドとして登録されているか
            if db.session.query(Friend).filter(Friend.user_id==current_user.id,Friend.friend_name==form.username.data).first():
                print("既に登録してるよ")
                print(db.session.query(Friend).filter(Friend.user_id==current_user.id).first())
                return redirect(url_for("chat.add_chat"))
            else:
                #フレンドを追加
                new_friends=[
                    {"user_id":current_user.id,"friend_name":search.username,"friend_user_id":search.id},
                    {"user_id":search.id,"friend_name":current_user.username,"friend_user_id":current_user.id}
                ]
                add_new_friend(new_friends)
                #チャット先を追加
                #個人チャットの場合は2つペアで存在するので/2をする
                #結果の数に+1をする　chat_idは1,2,3...という風になる
                count=db.session.query(Chat).filter(Chat.type=="Individual").count()/2 + db.session.query(Chat).filter(Chat.type=="Group").count() + 1
                new_chats=[
                    {"type":"Individual","user_id":current_user.id,"chat_name":search.username},
                    {"type":"Individual","user_id":search.id,"chat_name":current_user.username},
                ]
                create_new_chat(count,new_chats)
                #チャットメンバーを追加
                new_members=[
                    {"member_id":current_user.id,"member_name":current_user.username},
                    {"member_id":search.id,"member_name":search.username}
                ]
                add_new_chat_member(count,new_members)
                return redirect(url_for("chat.app"))
        print("アカウントが見つからないよ")
        return redirect(url_for("chat.add_chat"))

    return render_template("chat/add_chat.html",form=form)

@chat.route("/create_group",methods=["GET","POST"])
@login_required
def create_group():
    form = CreateGroupChatForm()
    #現在のフレンドを取得
    friends = db.session.query(Friend).filter(Friend.user_id==current_user.id).all()
    #選択肢に入れる
    form.friends.choices = [(str(friend.friend_user_id), friend.friend_name) for friend in friends]
    if form.validate_on_submit():
        count=db.session.query(Chat).filter(Chat.type=="Individual").count()/2 + db.session.query(Chat).filter(Chat.type=="Group").count() + 1
        new_chat = Chat(
            type="Group",
            chat_id=count,
            user_id=0,
            chat_name=form.name.data
        )
        db.session.add(new_chat)
        db.session.flush()
        #選択されたメンバーのIDを取得
        selected_members = form.friends.data
        new_members=[{"member_id":current_user.id,"member_name":current_user.username}]
        for member_id in selected_members:
            member = db.session.query(User).filter(User.id==member_id).first()
            new_members.append({"member_id":member.id,"member_name":member.username})
        add_new_chat_member(new_chat.chat_id,new_members)
        return redirect(url_for("chat.app"))

    return render_template("chat/create_group.html",form=form)

#登録されているチャットにメンバーを追加する関数
def add_new_chat_member(chat_id,chat_members):
    for member in chat_members:
        new_member=ChatMember(
            chat_id=chat_id,
            member_id=member["member_id"],
            member_name=member["member_name"]
        )
        db.session.add(new_member)
    db.session.commit()

def create_new_chat(chat_id,chats):
    for chat in chats:
        new_chat=Chat(
            chat_id=chat_id,
            type=chat["type"],
            user_id=chat["user_id"],
            chat_name=chat["chat_name"]
        )
        db.session.add(new_chat)
    db.session.commit()

def add_new_friend(friends):
    for friend in friends:
        new_friend=Friend(
            user_id=friend["user_id"],
            friend_name=friend["friend_name"],
            friend_user_id=friend["friend_user_id"]
        )
        db.session.add(new_friend)
    db.session.commit()

@socketio.on("chat")
def database_update(chat):
    send(chat,broadcast=True)

