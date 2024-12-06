from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField,SelectField,IntegerRangeField,DateField
from wtforms.validators import DataRequired,Length,InputRequired
from datetime import date

#ユーザー新規登録とユーザー編集フォームクラス
class ScheduleForm(FlaskForm):
    date = DateField(
        "日付",
        format="%Y-%m-%d",
        default=date.today,
        validators=[DataRequired("日付を入力してください。")]
    )

    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルを入力してください。"),
            Length(max=30,message="30文字以内で入力してください。")
        ]
    )

    memo = StringField(
        "メモ",
        validators=[
            Length(max=200,message="200文字以内で入力してください。")
        ]
    )

    link = StringField(
        "リンク",
        validators=[
            Length(max=100,message="100文字以内で入力してください。")
        ]
    )

    color = SelectField(
        "カラー",
        choices=[("red","赤"),
                 ("orange","橙"),
                 ("blue","青"),
                 ("green","緑"),
                 ("pink","桃"),
                 ("brown","茶")],
        default="red"
    )

    submit = SubmitField("追加")