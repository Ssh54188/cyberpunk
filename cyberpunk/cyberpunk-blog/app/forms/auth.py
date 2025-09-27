from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField('用户名/邮箱', validators=[DataRequired('请输入用户名或邮箱')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    """用户注册表单"""
    username = StringField('用户名', validators=[
        DataRequired('请输入用户名'),
        Length(min=2, max=50, message='用户名长度必须在2到50个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired('请输入邮箱'),
        Email('请输入有效的邮箱地址')
    ])
    password = PasswordField('密码', validators=[
        DataRequired('请输入密码'),
        Length(min=8, message='密码长度至少为8个字符')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired('请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        """验证用户名是否已存在"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用')
    
    def validate_email(self, email):
        """验证邮箱是否已存在"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被使用')

class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    current_password = PasswordField('当前密码', validators=[
        DataRequired('请输入当前密码')
    ])
    new_password = PasswordField('新密码', validators=[
        DataRequired('请输入新密码'),
        Length(min=8, message='新密码长度至少为8个字符')
    ])
    confirm_new_password = PasswordField('确认新密码', validators=[
        DataRequired('请确认新密码'),
        EqualTo('new_password', message='两次输入的新密码不一致')
    ])
    submit = SubmitField('修改密码')