from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid
from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(UserMixin, db.Model):
    """用户模型，包含用户的基本信息和认证相关功能"""
    __tablename__ = 'users'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'author', 'editor', 'admin'), default='user', nullable=False)
    nickname = db.Column(db.String(50))
    avatar_url = db.Column(db.String(500))
    bio = db.Column(db.Text)
    website = db.Column(db.String(200))
    github = db.Column(db.String(200))
    twitter = db.Column(db.String(200))
    location = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    last_login_at = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 权限字段
    can_publish = db.Column(db.Boolean, default=False)
    can_edit_other_posts = db.Column(db.Boolean, default=False)
    can_access_admin = db.Column(db.Boolean, default=False)
    can_manage_users = db.Column(db.Boolean, default=False)
    
    # 关系定义
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, **kwargs):
        """初始化用户对象，自动加密密码"""
        self.username = username
        self.email = email
        self.set_password(password)
        
        # 设置其他可选字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # 根据角色设置默认权限
        if self.role == 'admin':
            self.can_publish = True
            self.can_edit_other_posts = True
            self.can_access_admin = True
            self.can_manage_users = True
        elif self.role == 'editor':
            self.can_publish = True
            self.can_edit_other_posts = True
            self.can_access_admin = True
        elif self.role == 'author':
            self.can_publish = True
    
    def set_password(self, password):
        """设置用户密码，自动加密"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """验证用户密码是否正确"""
        return bcrypt.check_password_hash(self.password, password)
    
    def save(self):
        """保存用户到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新用户信息"""
        for key, value in kwargs.items():
            if key == 'password' and value:
                self.set_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)
                
        # 如果更新了角色，可能需要更新权限
        if 'role' in kwargs:
            if self.role == 'admin':
                self.can_publish = True
                self.can_edit_other_posts = True
                self.can_access_admin = True
                self.can_manage_users = True
            elif self.role == 'editor':
                self.can_publish = True
                self.can_edit_other_posts = True
                self.can_access_admin = True
            elif self.role == 'author':
                self.can_publish = True
        
        db.session.commit()
    
    def delete(self):
        """从数据库删除用户"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        """通过用户名查找用户"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        """通过邮箱查找用户"""
        return cls.query.filter_by(email=email).first()
    
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'
        
    def can_access_admin_panel(self):
        """检查用户是否可以访问管理后台"""
        return self.is_admin() or self.can_access_admin
        
    @hybrid_property
    def post_count(self):
        """获取用户发布的文章数量"""
        return len(self.posts)
        
    @hybrid_property
    def comment_count(self):
        """获取用户发布的评论数量"""
        return len(self.comments)
        
    @hybrid_property
    def display_name(self):
        """获取显示名称，优先使用昵称"""
        return self.nickname if self.nickname else self.username
    
    def __repr__(self):
        """返回用户的字符串表示"""
        return f'<User {self.username}>'