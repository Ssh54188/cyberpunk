# 导入所有模型类以便在其他地方统一引用
from app.models.user import User
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.models.comment import Comment
from app.models.page import Page
from app.models.setting import Setting

# 定义__all__来指定可以被import *导入的内容
__all__ = ['User', 'Post', 'Category', 'Tag', 'Comment', 'Page', 'Setting']