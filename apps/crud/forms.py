from flask_wtf import FlaskForm
from wtforms import PasswordField,IntegerField,StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,Length,NumberRange

#ユーザー新規登録とユーザー編集フォームクラス
class UserForm(FlaskForm):
    name = StringField(
        "氏名",
        validators=[
            DataRequired(message="氏名を入力してください。"),
            Length(max=30,message="30文字以内で入力してください。")
        ]
    )

    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired(message="ユーザー名を入力してください。"),
            Length(max=30,message="30文字以内で入力してください。")
        ]
    )

    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Email(message="メールアドレスの形式で入力してください。")
        ]
    )

    password = PasswordField(
        "パスワード",
        validators=[DataRequired(message="パスワードを入力してください。")]
    )

    #ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")