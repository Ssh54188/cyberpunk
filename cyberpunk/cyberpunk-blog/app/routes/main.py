from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.post import Post
from app.models.page import Page
from app.models.setting import Setting
from app.models.category import Category

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """网站首页"""
    # 获取最新的博客文章
    posts = Post.get_published_posts(limit=5)
    
    # 获取网站设置
    site_title = Setting.get_value('site_title', '赛博朋克博客')
    site_description = Setting.get_value('site_description', '一个赛博朋克风格的个人博客')
    
    # 获取分类列表
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('main/index.html', 
                          posts=posts, 
                          site_title=site_title, 
                          site_description=site_description,
                          categories=categories)

@main_bp.route('/about')
def about():
    """关于页面"""
    # 尝试从数据库获取关于页面内容
    about_page = Page.find_by_slug('about')
    
    if about_page and about_page.is_published:
        return render_template('main/page.html', page=about_page)
    else:
        # 如果数据库中没有关于页面，使用默认内容
        return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """联系页面"""
    # 尝试从数据库获取联系页面内容
    contact_page = Page.find_by_slug('contact')
    
    if contact_page and contact_page.is_published:
        return render_template('main/page.html', page=contact_page)
    else:
        # 如果数据库中没有联系页面，使用默认内容
        return render_template('main/contact.html')

@main_bp.route('/categories')
def categories():
    """分类列表页面 - 重定向到博客首页"""
    return redirect(url_for('blog.blog_index'))

@main_bp.route('/tags')
def tags():
    """标签列表页面 - 重定向到博客首页"""
    return redirect(url_for('blog.blog_index'))

@main_bp.route('/privacy')
def privacy():
    """隐私政策页面"""
    # 尝试从数据库获取隐私政策页面内容
    privacy_page = Page.find_by_slug('privacy')
    
    if privacy_page and privacy_page.is_published:
        return render_template('main/page.html', page=privacy_page)
    else:
        # 如果数据库中没有隐私政策页面，使用默认内容
        return render_template('main/privacy.html')

@main_bp.route('/terms')
def terms():
    """使用条款页面"""
    # 尝试从数据库获取使用条款页面内容
    terms_page = Page.find_by_slug('terms')
    
    if terms_page and terms_page.is_published:
        return render_template('main/page.html', page=terms_page)
    else:
        # 如果数据库中没有使用条款页面，使用默认内容
        return render_template('main/terms.html')

@main_bp.route('/search')
def search():
    """搜索页面"""
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        # 搜索文章和页面
        post_results = Post.query.filter(
            Post.is_published == True,
            (Post.title.like(f'%{query}%') | Post.content.like(f'%{query}%'))
        ).all()
        
        page_results = Page.query.filter(
            Page.is_published == True,
            (Page.title.like(f'%{query}%') | Page.content.like(f'%{query}%'))
        ).all()
        
        results = post_results + page_results
    
    return render_template('main/search.html', query=query, results=results)

@main_bp.route('/sitemap.xml')
def sitemap():
    """生成网站地图"""
    posts = Post.query.filter_by(is_published=True).all()
    pages = Page.query.filter_by(is_published=True).all()
    
    # 渲染XML模板
    response = render_template('main/sitemap.xml', posts=posts, pages=pages)
    return response, {'Content-Type': 'application/xml'}

@main_bp.context_processor
def inject_global_vars():
    """注入全局变量到模板中"""
    # 获取全局设置
    site_title = Setting.get_value('site_title', '赛博朋克博客')
    site_description = Setting.get_value('site_description', '')
    site_keywords = Setting.get_value('site_keywords', '')
    footer_text = Setting.get_value('footer_text', '')
    
    # 获取菜单页面
    menu_pages = Page.get_published_pages()
    
    return {
        'site_title': site_title,
        'site_description': site_description,
        'site_keywords': site_keywords,
        'footer_text': footer_text,
        'menu_pages': menu_pages,
        'current_user': current_user
    }