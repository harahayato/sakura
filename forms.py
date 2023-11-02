from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class InputForm(FlaskForm):
    line_file = FileField('LINEファイルの選択', validators = [DataRequired('LINEテキストファイルを選択してください')])
    your_name = StringField('あなたの名前：', validators = [DataRequired('必須入力です')], render_kw={"placeholder": "（例）恋愛　太郎"})
    partner_name = StringField('相手の名前：', validators = [DataRequired('必須入力です')], render_kw={"placeholder": "（例）恋愛　花子"})
    submit = SubmitField('診断する')
    
  