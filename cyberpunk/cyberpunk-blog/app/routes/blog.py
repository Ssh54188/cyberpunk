from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.models.comment import Comment
from app.forms.comment import CommentForm
from app import db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def blog_index():
    """博客文章列表页"""
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示的文章数量
    
    # 获取已发布的文章列表，支持分页
    posts = Post.query.filter_by(is_published=True).order_by(Post.published_at.desc())
    pagination = posts.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('blog/index.html', pagination=pagination)

@blog_bp.route('/<slug>')
def blog_post(slug):
    """博客文章详情页"""
    # 获取文章信息
    post = Post.find_by_slug(slug)
    
    if not post or not post.is_published:
        return render_template('errors/404.html'), 404
    
    # 增加文章浏览量
    post.increment_views()
    
    # 获取评论列表
    comments = Comment.get_comments_by_post(post.id)
    
    # 初始化评论表单
    comment_form = CommentForm()
    
    # 获取相关文章（同分类的其他文章）
    related_posts = Post.query.filter_by(category_id=post.category_id, is_published=True)
    related_posts = related_posts.filter(Post.id != post.id).limit(3).all()
    
    return render_template('blog/post.html', post=post, comments=comments, comment_form=comment_form, related_posts=related_posts)

@blog_bp.route('/category/<slug>')
def blog_category(slug):
    """分类文章列表页"""
    # 获取分类信息
    category = Category.find_by_slug(slug)
    
    if not category or not category.is_active:
        return render_template('errors/404.html'), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 获取该分类下的文章列表，支持分页
    posts = Post.query.filter_by(category_id=category.id, is_published=True).order_by(Post.published_at.desc())
    pagination = posts.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('blog/category.html', category=category, pagination=pagination)

@blog_bp.route('/tag/<slug>')
def blog_tag(slug):
    """标签文章列表页"""
    # 获取标签信息
    tag = Tag.find_by_slug(slug)
    
    if not tag or not tag.is_active:
        return render_template('errors/404.html'), 404
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 获取该标签下的文章列表，支持分页
    posts = tag.posts.filter_by(is_published=True).order_by(Post.published_at.desc())
    pagination = posts.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('blog/tag.html', tag=tag, pagination=pagination)

@blog_bp.route('/comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    """添加评论"""
    # 检查文章是否存在
    post = Post.query.get(post_id)
    
    if not post or not post.is_published:
        flash('文章不存在或未发布', 'danger')
        return redirect(url_for('blog.blog_index'))
    
    form = CommentForm()
    if form.validate_on_submit():
        content = form.content.data
        parent_id = form.parent_id.data if form.parent_id.data else None
        
        # 创建评论
        comment = Comment(
            content=content,
            post_id=post_id,
            author_id=current_user.id,
            parent_id=parent_id,
            is_approved=True  # 默认审核通过，可以根据需要改为False
        )
        comment.save()
        
        # 更新文章评论数
        post.comment_count += 1
        db.session.commit()
        
        flash('评论添加成功', 'success')
    else:
        flash('评论内容不能为空', 'danger')
    
    return redirect(url_for('blog.blog_post', slug=post.slug))

@blog_bp.route('/archives')
def archives():
    """文章归档页"""
    # 获取所有已发布的文章，按年份和月份分组
    posts = Post.query.filter_by(is_published=True).order_by(Post.published_at.desc()).all()
    
    # 按年份和月份组织文章
    archives_data = {}
    for post in posts:
        year = post.published_at.year
        month = post.published_at.month
        
        if year not in archives_data:
            archives_data[year] = {}
        
        if month not in archives_data[year]:
            archives_data[year][month] = []
        
        archives_data[year][month].append(post)
    
    return render_template('blog/archives.html', archives=archives_data)

@blog_bp.route('/popular')
def popular_posts():
    """热门文章列表"""
    # 获取浏览量最高的文章
    posts = Post.query.filter_by(is_published=True).order_by(Post.views_count.desc()).limit(10).all()
    
    return render_template('blog/popular.html', posts=posts)