# 赛博朋克风格个人博客网站文件清单

## 1. 项目根目录结构
```
cyberpunk-blog/              # 项目根目录，采用小写、连字符分隔的命名规范
├── app/                      # 主应用目录，所有核心代码存放于此
│   ├── __init__.py           # 应用初始化文件，创建和配置Flask应用实例
│   ├── models/               # 数据模型目录，映射数据库表结构
│   ├── routes/               # 路由目录，处理所有HTTP请求
│   ├── templates/            # 前端模板目录，存放Flask Templates文件
│   ├── static/               # 静态资源目录，存放CSS、JavaScript、图片等
│   ├── forms/                # 表单定义目录，处理用户输入验证
│   ├── utils/                # 工具函数目录，提供通用功能支持
│   └── admin/                # 管理员后台目录，包含后台相关功能
├── config.py                 # 应用配置文件，包含所有环境配置
├── requirements.txt          # 项目依赖文件，列出所有Python包依赖
├── run.py                    # 应用启动脚本，提供便捷的启动方式
├── migrations/               # 数据库迁移目录，管理数据库结构变更
├── tests/                    # 测试代码目录，存放单元测试和集成测试
├── README.md                 # 项目说明文档，包含项目介绍和使用指南
└── .gitignore                # Git忽略文件，指定不纳入版本控制的文件
```

## 2. 前端文件结构 (Flask Templates)
```
templates/                    # Flask Templates模板目录，采用分层组织
├── base.html                 # 基础模板文件，定义网站整体布局和通用元素
├── index.html                # 首页模板，继承自base.html，展示博客主页
├── auth/
│   ├── login.html            # 登录页面模板，处理用户登录表单
│   └── register.html         # 注册页面模板，处理新用户注册
├── posts/
│   ├── list.html             # 文章列表模板，展示多篇文章摘要
│   ├── detail.html           # 文章详情模板，展示单篇文章完整内容和评论
│   ├── create.html           # 创建文章模板，提供富文本编辑器
│   └── edit.html             # 编辑文章模板，用于修改已发布文章
├── admin/
│   ├── dashboard.html        # 管理员仪表盘模板，展示系统概览数据
│   ├── users.html            # 用户管理模板，管理注册用户信息
│   ├── posts.html            # 文章管理模板，批量管理博客文章
│   ├── comments.html         # 评论管理模板，审核和管理用户评论
│   ├── categories.html       # 分类管理模板，管理文章分类
│   ├── tags.html             # 标签管理模板，管理文章标签
│   └── settings.html         # 系统设置模板，配置网站参数
└── partials/
    ├── header.html           # 头部组件，包含导航栏和网站标识
    ├── sidebar.html          # 侧边栏组件，包含分类、标签和热门文章
    ├── footer.html           # 底部组件，包含版权信息和链接
    ├── flash_messages.html   # 消息提示组件，显示操作反馈信息
    └── pagination.html       # 分页组件，用于文章列表分页显示
```

## 3. 静态资源文件结构
```
static/                       # 静态资源目录，存放浏览器可直接访问的文件
├── css/                      # 样式文件目录，按功能模块组织
│   ├── main.css              # 主样式文件，定义基础样式规则
│   ├── cyberpunk.css         # 赛博朋克风格样式，实现霓虹、故障艺术等效果
│   ├── responsive.css        # 响应式设计样式，适配不同设备屏幕
│   ├── admin.css             # 管理员后台样式，提供专业管理界面
│   └── vendor/               # 第三方CSS库目录
│       ├── normalize.css     # 浏览器样式重置
│       └── highlight.css     # 代码高亮样式
├── js/
│   ├── main.js               # 主JavaScript文件，处理全局交互逻辑
│   ├── cyberpunk.js          # 赛博朋克特效脚本，实现视觉效果
│   ├── auth.js               # 认证相关脚本，处理登录注册交互
│   ├── admin.js              # 管理员后台脚本，增强管理功能
│   ├── editor.js             # 富文本编辑器配置和功能扩展
│   └── vendor/               # 第三方JavaScript库目录
│       ├── jquery.min.js     # jQuery库
│       └── chart.min.js      # 图表库
├── images/
│   ├── avatars/              # 用户头像目录，存储用户上传的头像
│   ├── featured/             # 特色图片目录，存储文章特色图片
│   ├── background/           # 背景图片目录
│   │   └── cyberpunk-bg.jpg  # 赛博朋克风格背景图
│   └── icons/                # 图标文件目录
│       ├── menu.svg          # 菜单图标
│       └── social/           # 社交媒体图标目录
└── fonts/
    └── vt323.ttf             # VT323字体文件，用于赛博朋克风格文字显示
```

## 4. 后端文件结构 (Flask应用)

### 4.1 应用初始化与配置
```
app/__init__.py               # Flask应用初始化，注册蓝图、配置扩展
config.py                     # 应用配置，包含数据库连接、密钥、环境变量等
run.py                        # 应用启动脚本，提供开发服务器启动入口
```

### 4.2 数据模型
```
app/models/
├── __init__.py               # 模型初始化，导入并注册所有模型
├── user.py                   # 用户模型，映射users表
├── post.py                   # 文章模型，映射posts表
├── category.py               # 分类模型，映射categories表
├── tag.py                    # 标签模型，映射tags表
├── comment.py                # 评论模型，映射comments表
├── page.py                   # 页面模型，映射pages表
├── setting.py                # 配置模型，映射settings表
├── attachment.py             # 附件模型，映射attachments表
└── activity_log.py           # 活动日志模型，映射activity_logs表
```

### 4.3 路由控制器
```
app/routes/
├── __init__.py               # 路由初始化，注册所有蓝图
├── main.py                   # 主路由，处理首页、关于页等静态页面
├── auth.py                   # 认证路由，处理登录、注册、登出等操作
├── user.py                   # 用户相关路由，处理用户个人资料、设置等
├── post.py                   # 文章相关路由，处理文章CRUD操作
├── comment.py                # 评论相关路由，处理评论提交和展示
└── api.py                    # API接口路由，使用Flask-RESTX提供RESTful API
```

### 4.4 管理员后台
```
app/admin/
├── __init__.py               # 后台初始化，创建和配置admin蓝图
├── views.py                  # 后台视图函数，实现管理界面逻辑
├── forms.py                  # 后台表单，用于管理操作的数据验证
├── utils.py                  # 后台工具函数，提供管理相关辅助功能
└── templates/                # 后台模板覆盖目录，用于自定义后台外观
```

### 4.5 表单定义
```
app/forms/
├── __init__.py               # 表单初始化，导入常用表单元素
├── auth.py                   # 认证表单，包含登录、注册等表单定义
├── post.py                   # 文章表单，包含文章创建、编辑等表单定义
├── user.py                   # 用户表单，包含用户信息修改等表单定义
└── comment.py                # 评论表单，包含评论提交表单定义
```

### 4.6 工具函数
```
app/utils/
├── __init__.py               # 工具初始化，提供通用工具函数导入
├── security.py               # 安全相关工具，包含密码加密、验证等功能
├── helpers.py                # 辅助函数，提供常用功能如日期格式化、文件处理等
├── validators.py             # 数据验证函数，实现自定义表单验证规则
├── cyberpunk_effects.py      # 赛博朋克效果工具函数，处理前端特效数据
├── email.py                  # 邮件发送工具，处理用户通知邮件
└── upload.py                 # 文件上传工具，处理图片等媒体文件上传
```

## 5. 数据库相关文件
```
migrations/                   # 数据库迁移文件目录，由Flask-Migrate自动生成
cyberpunk_blog.sql            # 数据库初始化SQL脚本，包含表结构和初始数据
```

## 6. 测试文件
```
tests/
├── __init__.py               # 测试初始化，配置测试环境
├── test_auth.py              # 认证功能测试，测试登录、注册等流程
├── test_posts.py             # 文章功能测试，测试文章CRUD操作
├── test_comments.py          # 评论功能测试，测试评论提交和展示
├── test_models.py            # 数据模型测试，测试数据库模型逻辑
├── test_utils.py             # 工具函数测试，测试辅助功能正确性
└── conftest.py               # 测试配置文件，提供测试夹具和共享配置
```

## 7. 部署相关文件
```
Dockerfile                    # Docker构建文件，定义应用容器化流程
.dockerignore                 # Docker忽略文件，排除不需要打包的文件
entrypoint.sh                 # 容器启动脚本，处理启动前准备工作
docker-compose.yml            # Docker Compose配置，定义多容器部署环境
nginx.conf                    # Nginx配置文件，提供反向代理和静态文件服务
uwsgi.ini                     # uWSGI配置文件，配置Python应用服务器
requirements-prod.txt         # 生产环境依赖文件，包含稳定版本依赖
.env.example                  # 环境变量示例文件，提供配置参考
```

## 8. 主要技术文件说明

### 8.1 前端技术文件
- **templates/base.html**: 定义网站整体结构和赛博朋克风格的基础样式，使用Flask Templates继承机制
- **static/css/cyberpunk.css**: 实现霓虹发光效果、故障艺术等赛博朋克视觉风格的核心样式文件
- **static/js/cyberpunk.js**: 实现动态背景、交互特效等前端交互功能的JavaScript文件
- **app/templates/**: 所有前端模板文件，基于Flask Templates实现服务端渲染
- **static/css/responsive.css**: 确保网站在不同设备上有良好显示效果的响应式样式

### 8.2 后端技术文件
- **app/__init__.py**: 初始化Flask应用、配置数据库连接、注册蓝图和扩展
- **app/models/**: 实现所有数据库模型，基于SQLAlchemy ORM与数据库结构对应
- **app/routes/**: 实现所有页面路由和API接口，采用蓝图组织不同功能模块
- **app/routes/api.py**: 使用Flask-RESTX实现的API接口，自动生成Swagger文档
- **config.py**: 包含开发、测试、生产等不同环境的配置信息，支持环境变量覆盖
- **app/utils/security.py**: 处理用户认证、密码加密等安全相关功能
- **app/forms/**: 定义表单验证规则，确保用户输入数据的合法性

### 8.3 依赖管理
- **requirements.txt**: 列出所有项目依赖，包括Flask、SQLAlchemy、Flask-Login、Flask-RESTX等核心框架
- **requirements-prod.txt**: 生产环境专用依赖文件，包含稳定版本的依赖库

### 8.4 部署配置文件
- **Dockerfile**: 定义Docker镜像构建流程，确保环境一致性
- **docker-compose.yml**: 配置多容器部署，包括应用服务、数据库和Nginx
- **nginx.conf**: 设置反向代理、静态资源缓存和HTTPS配置
- **uwsgi.ini**: 配置应用服务器参数，优化性能和稳定性

## 9. 项目结构说明

### 9.1 架构设计
该项目采用Flask框架的典型MVC架构设计，结合了服务端渲染和现代前端技术：
- **Model**: 由app/models/目录下的文件实现，负责数据存储和业务逻辑，基于SQLAlchemy ORM实现数据库操作
- **View**: 由app/templates/目录下的Flask Templates模板和static/目录下的前端资源实现，采用赛博朋克风格设计
- **Controller**: 由app/routes/目录下的视图函数实现，负责处理请求和返回响应，使用蓝图组织不同功能模块

### 9.2 命名规范
- **目录命名**: 采用小写、单数形式，使用连字符分隔（如`static-files`）
- **文件命名**: 采用小写、下划线分隔的命名方式（如`user_model.py`）
- **模块命名**: 遵循Python PEP8规范，使用小写、下划线分隔
- **类命名**: 采用驼峰命名法（如`UserModel`）
- **函数命名**: 采用小写、下划线分隔（如`create_user()`）

### 9.3 功能划分
项目按照功能模块进行清晰划分，主要包括：
- **认证模块**: 处理用户登录、注册、密码重置等功能（auth.py）
- **内容管理**: 处理文章、评论、分类、标签等内容相关功能（post.py, comment.py等）
- **用户管理**: 处理用户信息、权限、个人设置等功能（user.py）
- **后台管理**: 提供管理员专用的系统管理功能（admin/目录）
- **API服务**: 提供RESTful API接口，支持第三方应用集成（api.py）
- **工具支持**: 提供安全、文件上传、邮件发送等通用功能支持（utils/目录）

### 9.4 技术亮点
通过这种结构，实现了前后端分离但又紧密集成的开发模式，使用Python作为主要编程语言，既处理后端逻辑，又通过Flask Templates管理前端渲染。项目充分利用了Flask生态系统中的组件，如：
- Flask-Login: 用于用户认证和会话管理
- Flask-RESTX: 用于API接口开发和文档生成
- SQLAlchemy: 提供强大的ORM功能，简化数据库操作
- Flask-Migrate: 管理数据库结构变更和迁移
- Flask-WTF: 简化表单处理和验证

这种设计使得项目具有良好的可扩展性、可维护性和安全性，同时实现了功能完整的赛博朋克风格博客系统。