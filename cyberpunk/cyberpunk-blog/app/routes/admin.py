from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.user import User
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.models.comment import Comment
from app.models.page import Page
from app.models.setting import Setting
from app.forms.admin import PostForm, CategoryForm, TagForm, PageForm, SettingForm, UserForm
from app import db
import os
import uuid

admin_bp = Blueprint('admin', __name__)

# 管理员权限装饰器
def admin_required(f):
    """确保用户是管理员的装饰器"""
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('需要管理员权限', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    # 设置与原函数相同的名称，避免endpoint冲突
    decorated_function.__name__ = f.__name__
    decorated_function.__module__ = f.__module__
    decorated_function.__doc__ = f.__doc__
    return decorated_function

@admin_bp.route('/')
@admin_required
def admin_index():
    """管理员后台首页"""
    # 获取统计信息
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'total_published_posts': Post.query.filter_by(is_published=True).count(),
        'total_categories': Category.query.count(),
        'total_tags': Tag.query.count(),
        'total_comments': Comment.query.count(),
        'pending_comments': Comment.query.filter_by(is_approved=False).count(),
        'total_pages': Page.query.count()
    }
    
    # 获取最近的文章和评论
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    
    return render_template('admin/index.html', stats=stats, recent_posts=recent_posts, recent_comments=recent_comments)

@admin_bp.route('/posts')
@admin_required
def admin_posts():
    """文章列表管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 获取文章列表，支持分页和搜索
    search = request.args.get('search', '')
    query = Post.query
    
    if search:
        query = query.filter(
            (Post.title.like(f'%{search}%') | Post.content.like(f'%{search}%'))
        )
    
    pagination = query.order_by(Post.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/posts.html', pagination=pagination, search=search)

@admin_bp.route('/posts/create', methods=['GET', 'POST'])
@admin_required
def admin_posts_create():
    """创建新文章"""
    form = PostForm()
    
    if form.validate_on_submit():
        # 处理表单数据
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id,
            category_id=form.category_id.data,
            slug=form.slug.data,
            excerpt=form.excerpt.data,
            is_published=form.is_published.data,
            published_at=form.published_at.data if form.is_published.data else None
        )
        
        # 保存文章
        post.save()
        
        # 处理标签
        tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        
        db.session.commit()
        
        flash('文章创建成功', 'success')
        return redirect(url_for('admin.admin_posts'))
    
    return render_template('admin/post_create.html', form=form)

@admin_bp.route('/posts/edit/<id>', methods=['GET', 'POST'])
@admin_required
def admin_posts_edit(id):
    """编辑文章"""
    post = Post.query.get(id)
    
    if not post:
        flash('文章不存在', 'danger')
        return redirect(url_for('admin.admin_posts'))
    
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        # 更新文章数据
        form.populate_obj(post)
        
        # 处理发布时间
        if post.is_published and not post.published_at:
            post.published_at = db.func.current_timestamp()
        
        # 处理标签
        tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
        post.tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                post.tags.append(tag)
        
        db.session.commit()
        
        flash('文章更新成功', 'success')
        return redirect(url_for('admin.admin_posts'))
    
    # 设置当前选中的标签
    form.tags.data = [str(tag.id) for tag in post.tags]
    
    return render_template('admin/post_edit.html', form=form, post=post)

@admin_bp.route('/posts/delete/<id>', methods=['POST'])
@admin_required
def admin_posts_delete(id):
    """删除文章"""
    post = Post.query.get(id)
    
    if not post:
        flash('文章不存在', 'danger')
    else:
        post.delete()
        flash('文章已删除', 'success')
    
    return redirect(url_for('admin.admin_posts'))

@admin_bp.route('/categories')
@admin_required
def admin_categories():
    """分类管理"""
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@admin_required
def admin_categories_create():
    """创建新分类"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            slug=form.slug.data,
            description=form.description.data
        )
        category.save()
        
        flash('分类创建成功', 'success')
        return redirect(url_for('admin.admin_categories'))
    
    return render_template('admin/category_create.html', form=form)

@admin_bp.route('/categories/edit/<id>', methods=['GET', 'POST'])
@admin_required
def admin_categories_edit(id):
    """编辑分类"""
    category = Category.query.get(id)
    
    if not category:
        flash('分类不存在', 'danger')
        return redirect(url_for('admin.admin_categories'))
    
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.commit()
        
        flash('分类更新成功', 'success')
        return redirect(url_for('admin.admin_categories'))
    
    return render_template('admin/category_edit.html', form=form, category=category)

@admin_bp.route('/categories/delete/<id>', methods=['POST'])
@admin_required
def admin_categories_delete(id):
    """删除分类"""
    category = Category.query.get(id)
    
    if not category:
        flash('分类不存在', 'danger')
    else:
        # 检查是否有文章使用该分类
        if category.posts.count() > 0:
            flash('该分类下有文章，无法删除', 'danger')
        else:
            category.delete()
            flash('分类已删除', 'success')
    
    return redirect(url_for('admin.admin_categories'))

# 标签管理相关路由
@admin_bp.route('/tags')
@admin_required
def admin_tags():
    """标签管理"""
    tags = Tag.query.order_by(Tag.name.asc()).all()
    return render_template('admin/tags.html', tags=tags)

@admin_bp.route('/tags/create', methods=['GET', 'POST'])
@admin_required
def admin_tags_create():
    """创建新标签"""
    form = TagForm()
    
    if form.validate_on_submit():
        tag = Tag(
            name=form.name.data,
            slug=form.slug.data
        )
        tag.save()
        
        flash('标签创建成功', 'success')
        return redirect(url_for('admin.admin_tags'))
    
    return render_template('admin/tag_create.html', form=form)

@admin_bp.route('/tags/edit/<id>', methods=['GET', 'POST'])
@admin_required
def admin_tags_edit(id):
    """编辑标签"""
    tag = Tag.query.get(id)
    
    if not tag:
        flash('标签不存在', 'danger')
        return redirect(url_for('admin.admin_tags'))
    
    form = TagForm(obj=tag)
    
    if form.validate_on_submit():
        form.populate_obj(tag)
        db.session.commit()
        
        flash('标签更新成功', 'success')
        return redirect(url_for('admin.admin_tags'))
    
    return render_template('admin/tag_edit.html', form=form, tag=tag)

@admin_bp.route('/tags/delete/<id>', methods=['POST'])
@admin_required
def admin_tags_delete(id):
    """删除标签"""
    tag = Tag.query.get(id)
    
    if not tag:
        flash('标签不存在', 'danger')
    else:
        tag.delete()
        flash('标签已删除', 'success')
    
    return redirect(url_for('admin.admin_tags'))

# 用户管理相关路由
@admin_bp.route('/users')
@admin_required
def admin_users():
    """用户管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 获取搜索参数
    search = request.args.get('search', '')
    role = request.args.get('role', '')
    status = request.args.get('status', '')
    
    # 构建查询
    query = User.query
    
    # 搜索过滤
    if search:
        query = query.filter(
            (User.username.like(f'%{search}%') | 
             User.email.like(f'%{search}%') | 
             User.nickname.like(f'%{search}%'))
        )
    
    # 角色过滤
    if role:
        query = query.filter_by(role=role)
    
    # 状态过滤
    if status:
        # 注意：我们的模型使用的是is_active字段，需要映射到status参数
        if status == 'active':
            query = query.filter_by(is_active=True)
        elif status == 'inactive':
            query = query.filter_by(is_active=False)
    
    # 执行查询并分页
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/users/index.html', pagination=pagination, search=search, role=role, status=status)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@admin_required
def admin_add_user():
    """添加新用户"""
    form = UserForm()
    
    if form.validate_on_submit():
        # 创建新用户
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=form.role.data,
            is_active=form.status.data == 'active',
            nickname=form.nickname.data,
            website=form.website.data,
            # 其他字段根据我们的模型添加
            # 注意：我们需要映射表单字段到模型字段
        )
        
        # 保存用户到数据库
        user.save()
        
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.admin_users'))
    
    return render_template('admin/users/edit.html', form=form, title='添加新用户')

@admin_bp.route('/users/edit/<id>', methods=['GET', 'POST'])
@admin_required
def admin_users_edit(id):
    """编辑用户"""
    user = User.query.get(id)
    
    if not user:
        flash('用户不存在', 'danger')
        return redirect(url_for('admin.admin_users'))
    
    # 不允许修改当前登录的管理员角色
    if user.id == current_user.id and user.role == 'admin':
        readonly_admin = True
    else:
        readonly_admin = False
    
    form = UserForm(obj=user)
    
    # 设置状态字段的值
    form.status.data = 'active' if user.is_active else 'inactive'
    
    if form.validate_on_submit():
        # 更新用户基本信息
        user.email = form.email.data
        user.role = form.role.data
        user.is_active = form.status.data == 'active'
        user.nickname = form.nickname.data
        user.website = form.website.data
        
        # 如果有设置新密码
        if form.password.data:
            user.set_password(form.password.data)
        
        # 保存更改
        db.session.commit()
        
        flash('用户信息已更新', 'success')
        return redirect(url_for('admin.admin_users'))
    
    return render_template('admin/users/edit.html', form=form, user=user, title='编辑用户', readonly_admin=readonly_admin)

@admin_bp.route('/users/delete/<id>', methods=['POST'])
@admin_required
def admin_users_delete(id):
    """删除用户"""
    # 不允许删除当前登录的管理员
    if id == current_user.id:
        flash('不允许删除当前登录的管理员', 'danger')
        return redirect(url_for('admin.admin_users'))
    
    user = User.query.get(id)
    
    if not user:
        flash('用户不存在', 'danger')
    else:
        try:
            # 先处理用户相关的内容
            # 删除用户的文章
            for post in user.posts:
                db.session.delete(post)
            
            # 删除用户的评论
            for comment in user.comments:
                db.session.delete(comment)
            
            # 删除用户自身
            db.session.delete(user)
            db.session.commit()
            
            flash('用户已删除', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'删除用户时出错: {str(e)}', 'danger')
    
    return redirect(url_for('admin.admin_users'))

# 评论管理相关路由
@admin_bp.route('/comments')
@admin_required
def admin_comments():
    """评论管理"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 支持按审核状态筛选
    status = request.args.get('status', 'all')
    query = Comment.query
    
    if status == 'approved':
        query = query.filter_by(is_approved=True)
    elif status == 'pending':
        query = query.filter_by(is_approved=False)
    
    comments = query.order_by(Comment.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/comments.html', pagination=comments, status=status)

@admin_bp.route('/comments/approve/<id>', methods=['POST'])
@admin_required
def admin_comments_approve(id):
    """审核通过评论"""
    comment = Comment.query.get(id)
    
    if not comment:
        flash('评论不存在', 'danger')
    else:
        comment.approve()
        flash('评论已审核通过', 'success')
    
    return redirect(url_for('admin.admin_comments'))

@admin_bp.route('/comments/delete/<id>', methods=['POST'])
@admin_required
def admin_comments_delete(id):
    """删除评论"""
    comment = Comment.query.get(id)
    
    if not comment:
        flash('评论不存在', 'danger')
    else:
        comment.delete()
        flash('评论已删除', 'success')
    
    return redirect(url_for('admin.admin_comments'))

# 页面管理相关路由
@admin_bp.route('/pages')
@admin_required
def admin_pages():
    """页面管理"""
    pages = Page.query.order_by(Page.menu_order.asc()).all()
    return render_template('admin/pages.html', pages=pages)

@admin_bp.route('/pages/create', methods=['GET', 'POST'])
@admin_required
def admin_pages_create():
    """创建新页面"""
    form = PageForm()
    
    if form.validate_on_submit():
        page = Page(
            title=form.title.data,
            content=form.content.data,
            slug=form.slug.data,
            show_in_menu=form.show_in_menu.data,
            menu_order=form.menu_order.data,
            is_published=form.is_published.data
        )
        page.save()
        
        flash('页面创建成功', 'success')
        return redirect(url_for('admin.admin_pages'))
    
    return render_template('admin/page_create.html', form=form)

@admin_bp.route('/pages/edit/<id>', methods=['GET', 'POST'])
@admin_required
def admin_pages_edit(id):
    """编辑页面"""
    page = Page.query.get(id)
    
    if not page:
        flash('页面不存在', 'danger')
        return redirect(url_for('admin.admin_pages'))
    
    form = PageForm(obj=page)
    
    if form.validate_on_submit():
        form.populate_obj(page)
        db.session.commit()
        
        flash('页面更新成功', 'success')
        return redirect(url_for('admin.admin_pages'))
    
    return render_template('admin/page_edit.html', form=form, page=page)

@admin_bp.route('/pages/delete/<id>', methods=['POST'])
@admin_required
def admin_pages_delete(id):
    """删除页面"""
    page = Page.query.get(id)
    
    if not page:
        flash('页面不存在', 'danger')
    else:
        page.delete()
        flash('页面已删除', 'success')
    
    return redirect(url_for('admin.admin_pages'))

# 网站设置相关路由
@admin_bp.route('/settings')
@admin_required
def admin_settings():
    """网站设置"""
    settings = Setting.query.order_by(Setting.key.asc()).all()
    return render_template('admin/settings.html', settings=settings)

@admin_bp.route('/settings/edit/<key>', methods=['GET', 'POST'])
@admin_required
def admin_settings_edit(key):
    """编辑设置"""
    setting = Setting.query.filter_by(key=key).first()
    
    if not setting:
        flash('设置不存在', 'danger')
        return redirect(url_for('admin.admin_settings'))
    
    form = SettingForm(obj=setting)
    
    if form.validate_on_submit():
        form.populate_obj(setting)
        db.session.commit()
        
        flash('设置已更新', 'success')
        return redirect(url_for('admin.admin_settings'))
    
    return render_template('admin/setting_edit.html', form=form, setting=setting)

@admin_bp.route('/settings/add', methods=['GET', 'POST'])
@admin_required
def admin_settings_add():
    """添加新设置"""
    form = SettingForm()
    
    if form.validate_on_submit():
        # 检查设置键是否已存在
        if Setting.query.filter_by(key=form.key.data).first():
            flash('设置键已存在', 'danger')
            return redirect(url_for('admin.admin_settings_add'))
        
        setting = Setting(
            key=form.key.data,
            value=form.value.data,
            description=form.description.data,
            type=form.type.data,
            is_active=form.is_active.data
        )
        setting.save()
        
        flash('设置已添加', 'success')
        return redirect(url_for('admin.admin_settings'))
    
    return render_template('admin/setting_add.html', form=form)