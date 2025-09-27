from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length

class CommentForm(FlaskForm):
    """博客文章评论表单"""
    content = TextAreaField('评论内容', validators=[
        DataRequired('请输入评论内容'),
        Length(min=1, max=1000, message='评论内容长度必须在1到1000个字符之间')
    ])
    parent_id = HiddenField('父评论ID')  # 用于回复功能
    submit = SubmitField('发表评论')