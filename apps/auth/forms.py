from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email,Length

class SignUpForm(FlaskForm):
    name = StringField(
        "本名",
        validators=[
            DataRequired("本名を入力してください"),
            Length(1,30,"30文字以内で入力してください。")
        ]
    )
    username = StringField(
        "ユーザー名",
        validators=[
            DataRequired("ユーザー名を入力してください"),
            Length(1,20,"20文字以内で入力してください。")
        ]
    )
    if_ProjectLeader = SelectField(
        "あなたはプロジェクトリーダーですか。",
        choices=[
            ("true", "はい"),
            ("false", "いいえ")
        ],
        coerce=lambda x: x == "true"  # boolean型に変換
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスを入力してください"),
            Email("メールアドレスの形式で入力してください。")
        ]
    )
    password = PasswordField("パスワード",
        validators=[DataRequired("パスワードを入力してください")])
    submit = SubmitField("新規登録")

class LoginForm(FlaskForm):
    username = StringField(
        "メールアドレス",
        validators=[
            DataRequired("ユーザー名を入力してください。"),
        ]
    )
    password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードを入力してください。")])
    submit = SubmitField("ログイン")