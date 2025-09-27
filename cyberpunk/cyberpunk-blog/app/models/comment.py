from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from app import db

class Comment(db.Model):
    """博客文章评论模型"""
    __tablename__ = 'comments'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    content = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 外键
    post_id = db.Column(db.String(50), db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.String(50), db.ForeignKey('comments.id'))  # 用于回复功能
    
    # 自引用关系（回复功能）
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, content, post_id, author_id, **kwargs):
        """初始化评论对象"""
        self.content = content
        self.post_id = post_id
        self.author_id = author_id
        
        # 设置其他可选字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def save(self):
        """保存评论到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新评论信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """从数据库删除评论"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_comments_by_post(cls, post_id, approved=True):
        """获取指定文章的评论列表"""
        query = cls.query.filter_by(post_id=post_id)
        if approved:
            query = query.filter_by(is_approved=True)
        return query.order_by(cls.created_at.asc()).all()
    
    @classmethod
    def get_pending_comments(cls):
        """获取待审核的评论列表"""
        return cls.query.filter_by(is_approved=False).order_by(cls.created_at.desc()).all()
    
    def approve(self):
        """审核通过评论"""
        self.is_approved = True
        db.session.commit()
    
    def __repr__(self):
        """返回评论的字符串表示"""
        return f'<Comment on Post {self.post_id}>'