from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime
from app.models.category import Category
from app.models.tag import Tag

class PostForm(FlaskForm):
    """博客文章表单"""
    title = StringField('标题', validators=[
        DataRequired('请输入标题'),
        Length(min=1, max=200, message='标题长度必须在1到200个字符之间')
    ])
    slug = StringField('Slug', validators=[
        DataRequired('请输入Slug'),
        Length(min=1, max=200, message='Slug长度必须在1到200个字符之间')
    ])
    content = TextAreaField('内容', validators=[
        DataRequired('请输入内容')
    ])
    excerpt = TextAreaField('摘要')
    category_id = SelectField('分类', coerce=str, validators=[DataRequired('请选择分类')])
    tags = SelectMultipleField('标签', coerce=str)
    is_published = BooleanField('发布')
    published_at = StringField('发布时间')  # 在模板中使用日期时间选择器
    submit = SubmitField('保存')
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # 动态加载分类选项
        self.category_id.choices = [(cat.id, cat.name) for cat in Category.query.filter_by(is_active=True).all()]
        # 动态加载标签选项
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.filter_by(is_active=True).all()]
    
    def validate_slug(self, slug):
        """验证Slug是否唯一（编辑时排除当前文章）"""
        from app.models.post import Post
        post_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_post = Post.query.filter_by(slug=slug.data).first()
        if existing_post and existing_post.id != post_id:
            raise ValidationError('该Slug已被使用')

class CategoryForm(FlaskForm):
    """文章分类表单"""
    name = StringField('名称', validators=[
        DataRequired('请输入名称'),
        Length(min=1, max=50, message='名称长度必须在1到50个字符之间')
    ])
    slug = StringField('Slug', validators=[
        DataRequired('请输入Slug'),
        Length(min=1, max=50, message='Slug长度必须在1到50个字符之间')
    ])
    description = TextAreaField('描述')
    submit = SubmitField('保存')
    
    def validate_name(self, name):
        """验证名称是否唯一（编辑时排除当前分类）"""
        category_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_category = Category.query.filter_by(name=name.data).first()
        if existing_category and existing_category.id != category_id:
            raise ValidationError('该分类名称已被使用')
    
    def validate_slug(self, slug):
        """验证Slug是否唯一（编辑时排除当前分类）"""
        category_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_category = Category.query.filter_by(slug=slug.data).first()
        if existing_category and existing_category.id != category_id:
            raise ValidationError('该Slug已被使用')

class TagForm(FlaskForm):
    """文章标签表单"""
    name = StringField('名称', validators=[
        DataRequired('请输入名称'),
        Length(min=1, max=30, message='名称长度必须在1到30个字符之间')
    ])
    slug = StringField('Slug', validators=[
        DataRequired('请输入Slug'),
        Length(min=1, max=30, message='Slug长度必须在1到30个字符之间')
    ])
    submit = SubmitField('保存')
    
    def validate_name(self, name):
        """验证名称是否唯一（编辑时排除当前标签）"""
        from app.models.tag import Tag
        tag_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_tag = Tag.query.filter_by(name=name.data).first()
        if existing_tag and existing_tag.id != tag_id:
            raise ValidationError('该标签名称已被使用')
    
    def validate_slug(self, slug):
        """验证Slug是否唯一（编辑时排除当前标签）"""
        from app.models.tag import Tag
        tag_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_tag = Tag.query.filter_by(slug=slug.data).first()
        if existing_tag and existing_tag.id != tag_id:
            raise ValidationError('该Slug已被使用')

class PageForm(FlaskForm):
    """静态页面对表单"""
    title = StringField('标题', validators=[
        DataRequired('请输入标题'),
        Length(min=1, max=200, message='标题长度必须在1到200个字符之间')
    ])
    slug = StringField('Slug', validators=[
        DataRequired('请输入Slug'),
        Length(min=1, max=200, message='Slug长度必须在1到200个字符之间')
    ])
    content = TextAreaField('内容', validators=[
        DataRequired('请输入内容')
    ])
    show_in_menu = BooleanField('显示在菜单')
    menu_order = IntegerField('菜单顺序', default=0)
    is_published = BooleanField('发布')
    submit = SubmitField('保存')
    
    def validate_slug(self, slug):
        """验证Slug是否唯一（编辑时排除当前页面）"""
        from app.models.page import Page
        page_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_page = Page.query.filter_by(slug=slug.data).first()
        if existing_page and existing_page.id != page_id:
            raise ValidationError('该Slug已被使用')

class SettingForm(FlaskForm):
    """网站设置表单"""
    key = StringField('设置键', validators=[
        DataRequired('请输入设置键'),
        Length(min=1, max=50, message='设置键长度必须在1到50个字符之间')
    ])
    value = TextAreaField('设置值', validators=[DataRequired('请输入设置值')])
    description = TextAreaField('描述')
    type = SelectField('类型', choices=[
        ('string', '字符串'),
        ('text', '文本'),
        ('boolean', '布尔值'),
        ('number', '数字')
    ], default='string')
    is_active = BooleanField('启用', default=True)
    submit = SubmitField('保存')
    
    def validate_key(self, key):
        """验证设置键是否唯一（编辑时排除当前设置）"""
        from app.models.setting import Setting
        setting_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_setting = Setting.query.filter_by(key=key.data).first()
        if existing_setting and existing_setting.id != setting_id:
            raise ValidationError('该设置键已被使用')

class UserForm(FlaskForm):
    """用户管理表单"""
    username = StringField('用户名', validators=[
        DataRequired('请输入用户名'),
        Length(min=3, max=50, message='用户名长度必须在3到50个字符之间')
    ])
    email = StringField('电子邮箱', validators=[
        DataRequired('请输入电子邮箱'),
        Length(min=5, max=100, message='电子邮箱长度必须在5到100个字符之间')
    ])
    password = StringField('密码')
    confirm_password = StringField('确认密码')
    role = SelectField('用户角色', choices=[
        ('user', '普通用户'),
        ('author', '作者'),
        ('editor', '编辑'),
        ('admin', '管理员')
    ], default='user', validators=[DataRequired('请选择用户角色')])
    status = SelectField('用户状态', choices=[
        ('active', '已激活'),
        ('inactive', '已禁用'),
        ('pending', '待审核')
    ], default='active', validators=[DataRequired('请选择用户状态')])
    nickname = StringField('昵称', validators=[
        Length(max=50, message='昵称长度不能超过50个字符')
    ])
    website = StringField('个人网站')
    github = StringField('GitHub')
    twitter = StringField('Twitter/X')
    can_publish = BooleanField('允许发布文章')
    can_edit_other_posts = BooleanField('允许编辑他人文章')
    can_access_admin = BooleanField('允许访问管理后台')
    can_manage_users = BooleanField('允许管理用户')
    submit = SubmitField('保存')
    
    def validate_username(self, username):
        """验证用户名是否唯一（编辑时排除当前用户）"""
        from app.models.user import User
        user_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_user = User.find_by_username(username.data)
        if existing_user and existing_user.id != user_id:
            raise ValidationError('该用户名已被使用')
            
    def validate_email(self, email):
        """验证电子邮箱是否唯一（编辑时排除当前用户）"""
        from app.models.user import User
        user_id = self._obj.id if hasattr(self._obj, 'id') else None
        existing_user = User.find_by_email(email.data)
        if existing_user and existing_user.id != user_id:
            raise ValidationError('该电子邮箱已被使用')
            
    def validate(self):
        """验证表单数据，包括密码一致性检查"""
        if not super(UserForm, self).validate():
            return False
            
        # 如果填写了密码，检查密码一致性
        if self.password.data or self.confirm_password.data:
            if self.password.data != self.confirm_password.data:
                self.confirm_password.errors.append('两次输入的密码不一致')
                return False
            
            # 密码强度检查
            if len(self.password.data) < 8:
                self.password.errors.append('密码长度至少为8位')
                return False
                
            # 密码必须包含字母和数字
            if not any(char.isalpha() for char in self.password.data) or not any(char.isdigit() for char in self.password.data):
                self.password.errors.append('密码必须包含字母和数字')
                return False
        
        return True