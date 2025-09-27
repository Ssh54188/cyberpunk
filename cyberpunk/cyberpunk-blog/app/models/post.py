from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from app import db
from app.models.tag import post_tags

class Post(db.Model):
    """博客文章模型"""
    __tablename__ = 'posts'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=False, nullable=False)
    published_at = db.Column(db.TIMESTAMP)
    views_count = db.Column(db.Integer, default=0, nullable=False)
    comment_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 外键
    author_id = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.String(50), db.ForeignKey('categories.id'), nullable=False)
    
    # 关系定义
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, title, content, author_id, category_id, slug, **kwargs):
        """初始化文章对象"""
        self.title = title
        self.content = content
        self.author_id = author_id
        self.category_id = category_id
        self.slug = slug
        
        # 设置其他可选字段
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def save(self):
        """保存文章到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新文章信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """从数据库删除文章"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def find_by_slug(cls, slug):
        """通过slug查找文章"""
        return cls.query.filter_by(slug=slug).first()
    
    @classmethod
    def get_published_posts(cls, limit=None, offset=0):
        """获取已发布的文章列表"""
        query = cls.query.filter_by(is_published=True).order_by(cls.published_at.desc())
        if limit:
            query = query.limit(limit).offset(offset)
        return query.all()
    
    @classmethod
    def get_posts_by_category(cls, category_id, limit=None, offset=0):
        """获取指定分类的文章列表"""
        query = cls.query.filter_by(category_id=category_id, is_published=True).order_by(cls.published_at.desc())
        if limit:
            query = query.limit(limit).offset(offset)
        return query.all()
    
    @classmethod
    def get_posts_by_tag(cls, tag_id, limit=None, offset=0):
        """获取指定标签的文章列表"""
        from app.models.tag import Tag
        tag = Tag.query.get(tag_id)
        if tag:
            query = tag.posts.filter_by(is_published=True).order_by(cls.published_at.desc())
            if limit:
                query = query.limit(limit).offset(offset)
            return query.all()
        return []
    
    def increment_views(self):
        """增加文章浏览量"""
        self.views_count += 1
        db.session.commit()
    
    def __repr__(self):
        """返回文章的字符串表示"""
        return f'<Post {self.title}>'