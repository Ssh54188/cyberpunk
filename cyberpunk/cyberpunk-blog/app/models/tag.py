from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from app import db

# 文章和标签的多对多关联表
post_tags = db.Table('post_tags',
    db.Column('post_id', db.String(50), db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.String(50), db.ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    """博客文章标签模型"""
    __tablename__ = 'tags'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(30), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(30), unique=True, nullable=False, index=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关系定义（通过关联表实现多对多）
    posts = db.relationship('Post', secondary=post_tags, backref=db.backref('tags', lazy='dynamic'))
    
    def __init__(self, name, slug, **kwargs):
        """初始化标签对象"""
        self.name = name
        self.slug = slug
        
        # 设置其他可选字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def save(self):
        """保存标签到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新标签信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """从数据库删除标签"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_name(cls, name):
        """通过名称查找标签"""
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_slug(cls, slug):
        """通过slug查找标签"""
        return cls.query.filter_by(slug=slug).first()
    
    def __repr__(self):
        """返回标签的字符串表示"""
        return f'<Tag {self.name}>'