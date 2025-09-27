from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from app import db

class Page(db.Model):
    """静态页面模型"""
    __tablename__ = 'pages'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    show_in_menu = db.Column(db.Boolean, default=True, nullable=False)
    menu_order = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, title, content, slug, **kwargs):
        """初始化页面对象"""
        self.title = title
        self.content = content
        self.slug = slug
        
        # 设置其他可选字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def save(self):
        """保存页面到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新页面信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """从数据库删除页面"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_slug(cls, slug):
        """通过slug查找页面"""
        return cls.query.filter_by(slug=slug).first()
    
    @classmethod
    def get_published_pages(cls, include_in_menu=True):
        """获取已发布的页面列表"""
        query = cls.query.filter_by(is_published=True)
        if include_in_menu:
            query = query.filter_by(show_in_menu=True)
        return query.order_by(cls.menu_order.asc()).all()
    
    def __repr__(self):
        """返回页面的字符串表示"""
        return f'<Page {self.title}>'