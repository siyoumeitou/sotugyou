from flask_wtf import FlaskForm
from wtforms import PasswordField,IntegerField,StringField,SubmitField,SelectField,SelectMultipleField,widgets
from wtforms.validators import DataRequired,Email,Length,NumberRange

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)  # リスト表示形式
    option_widget = widgets.CheckboxInput()  # 各選択肢をチェックボックスとして表示

#ユーザー新規登録とユーザー編集フォームクラス
class AddChatForm(FlaskForm):
    username = StringField(
        "アカウント名",
        validators=[
            DataRequired(message="アカウント名を入力してください。"),
            Length(max=30,message="30文字以内で入力してください。")
        ]
    )
    submit = SubmitField("追加")

class ChatForm(FlaskForm):
    chat = StringField(
        "入力",
        validators=[
            DataRequired(message="文面を入力してください。"),
            Length(max=200,message="200文字以内で入力してください。")
        ]
    )
    submit = SubmitField("送信")

class CreateGroupChatForm(FlaskForm):
    name = StringField(
        "グループ名",
        validators=[
            DataRequired(message="グループ名を入力してください。"),
            Length(max=30,message="30文字以内で入力してください。")
        ]
    )
    friends = MultiCheckboxField("グループメンバー")
    submit = SubmitField("作成")