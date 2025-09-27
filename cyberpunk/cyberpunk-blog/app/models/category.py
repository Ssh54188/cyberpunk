from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from app import db

class Category(db.Model):
    """博客文章分类模型"""
    __tablename__ = 'categories'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关系定义
    posts = db.relationship('Post', backref='category', lazy=True)
    
    def __init__(self, name, slug, **kwargs):
        """初始化分类对象"""
        self.name = name
        self.slug = slug
        
        # 设置其他可选字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def save(self):
        """保存分类到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新分类信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """从数据库删除分类"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_name(cls, name):
        """通过名称查找分类"""
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_slug(cls, slug):
        """通过slug查找分类"""
        return cls.query.filter_by(slug=slug).first()
    
    def __repr__(self):
        """返回分类的字符串表示"""
        return f'<Category {self.name}>'