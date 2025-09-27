from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.auth import LoginForm, RegistrationForm, ChangePasswordForm
from app import db
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        
        user = User.find_by_username(username)
        # 如果找不到用户名，尝试通过邮箱查找
        if not user:
            user = User.find_by_email(username)
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('账号已被禁用，请联系管理员', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=remember)
            user.last_login_at = db.func.current_timestamp()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # 检查用户名和邮箱是否已存在
        if User.find_by_username(username):
            flash('用户名已被使用', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.find_by_email(email):
            flash('邮箱已被使用', 'danger')
            return redirect(url_for('auth.register'))
        
        # 创建新用户
        user = User(username=username, email=email, password=password)
        user.save()
        
        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        
        # 验证当前密码
        if not current_user.check_password(current_password):
            flash('当前密码错误', 'danger')
            return redirect(url_for('auth.change_password'))
        
        # 更新密码
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('密码修改成功', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/profile')
@login_required
def profile():
    """用户个人资料"""
    return render_template('auth/profile.html', user=current_user)

@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑用户个人资料"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        bio = request.form.get('bio')
        website = request.form.get('website')
        location = request.form.get('location')
        
        # 验证用户名是否已存在
        if username != current_user.username and User.find_by_username(username):
            flash('用户名已被使用', 'danger')
            return redirect(url_for('auth.edit_profile'))
        
        # 验证邮箱是否已存在
        if email != current_user.email and User.find_by_email(email):
            flash('邮箱已被使用', 'danger')
            return redirect(url_for('auth.edit_profile'))
        
        # 更新资料
        current_user.update(
            username=username,
            email=email,
            bio=bio,
            website=website,
            location=location
        )
        
        flash('个人资料更新成功', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', user=current_user)