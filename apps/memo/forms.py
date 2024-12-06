from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length

#ユーザー新規登録とユーザー編集フォームクラス
class CreateMemoForm(FlaskForm):
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルを入力してください。"),
            Length(max=50,message="50文字以内で入力してください。")
        ]
    )

    memo = TextAreaField(
        "本文",
        validators=[
            Length(max=500,message="500文字以内で入力してください。")
        ]
    )

    folder = SelectField(
        "フォルダー",
        choices=[
            (0,"選択しない")
        ],
        default=0
    )
    
    submit = SubmitField("作成")

class CreateFolderForm(FlaskForm):
    name = StringField(
        "フォルダ名",
        validators=[
            DataRequired(message="フォルダ名を入力してください。"),
            Length(max=30,message="30文字以内で入力してください。")
        ]
    )
    submit = SubmitField("作成")