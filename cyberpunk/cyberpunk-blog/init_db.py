# 从.env文件加载环境变量
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import User, Post, Category, Tag, Comment, Page, Setting

# 创建应用实例
app = create_app()

# 在应用上下文中执行数据库操作
with app.app_context():
    # 创建数据库表
    db.create_all()
    
    # 检查是否已有管理员用户，如果没有则创建
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password='Admin123!',
            role='admin',
            is_active=True,
            email_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print('管理员用户已创建：用户名=admin，密码=Admin123!')
    
    # 创建默认分类
    default_category = Category.query.filter_by(name='未分类').first()
    if not default_category:
        default_category = Category(name='未分类', slug='uncategorized', description='默认分类')
        db.session.add(default_category)
        db.session.commit()
        print('默认分类已创建')
    
    print('数据库初始化完成')