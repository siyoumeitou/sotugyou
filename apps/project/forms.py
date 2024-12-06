from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,SubmitField,SelectField,SelectMultipleField, widgets
from wtforms.validators import DataRequired,Email,Length,NumberRange

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)  # リスト表示形式
    option_widget = widgets.CheckboxInput()  # 各選択肢をチェックボックスとして表示

#プロジェクト作成クラス
class ProjectCreateForm(FlaskForm):
    name = StringField(
        "プロジェクト名",
        validators=[
            DataRequired(message="プロジェクト名を入力してください。"),
            Length(max=100,message="100文字以内で入力してください。")
        ]
    )

    comment = StringField(
        "詳細",
        validators=[
            Length(max=500,message="500文字以内で入力してください。")
        ]
    )

    friends = MultiCheckboxField("プロジェクトメンバー")

    #ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")

class TaskCreateForm(FlaskForm):
    name = StringField(
        "タスク名",
        validators=[
            DataRequired(message="タスク名を入力してください。"),
            Length(max=50,message="50文字以内で入力してください。")
        ]
    )

    description = StringField(
        "作業内容",
        validators=[
            DataRequired(message="作業内容を入力してください。"),
            Length(max=500,message="500文字以内で入力してください。")
        ]
    )

    comment = StringField(
        "詳細",
        validators=[
            Length(max=500,message="500文字以内で入力してください。")
        ]
    )

    #ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("新規登録")

class TasksProgerssFrom(FlaskForm):
    name = StringField(
        "作業内容",
        validators=[
            DataRequired(message="作業内容を入力してください。"),
            Length(max=100,message="100文字以内で入力してください。")
        ]
    )

    progress = StringField(
        "進捗",
        validators=[
            DataRequired(message="進捗を入力してください。"),
            Length(max=500,message="500文字以内で入力してください。")
        ]
    )

    comment = StringField(
        "詳細",
        validators=[
            Length(max=500,message="500文字以内で入力してください。")
        ]
    )

    percent = IntegerField(
        "進捗割合",
        validators=[
            DataRequired(),
            NumberRange(min=0,max=100,message="0~100の間で入力してください。")
        ]
    )
    #ユーザーフォームsubmitの文言を設定する
    submit = SubmitField("進捗登録")