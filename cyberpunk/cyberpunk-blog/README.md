# 赛博朋克风格博客系统

一个具有强烈赛博朋克视觉风格的现代化博客管理系统，结合了先进的前端设计和稳健的后端架构。

## 功能特性

### 管理后台功能
- ✨ 文章管理：创建、编辑、发布和删除文章
- 🗂️ 分类管理：创建和管理文章分类
- 🏷️ 标签管理：创建和管理文章标签
- 👥 用户管理：创建和管理系统用户，支持多种用户角色
- 🔍 搜索和筛选：快速查找内容
- 📱 响应式设计：适配各种屏幕尺寸
- 💫 赛博朋克风格UI：霓虹灯效果、故障艺术、未来感设计

### 博客前台功能
- 📝 文章展示：优雅地展示博客文章
- 📊 分类浏览：按分类浏览文章
- 🏷️ 标签筛选：通过标签筛选相关文章
- 💬 评论系统：支持读者评论互动
- 🔍 全站搜索：快速查找感兴趣的内容

## 技术栈

- **后端框架**：Flask (Python)
- **数据库**：SQLAlchemy ORM + MySQL/SQLite
- **前端技术**：HTML5, CSS3, JavaScript, Bootstrap
- **认证系统**：Flask-Login
- **表单处理**：Flask-WTF
- **密码加密**：Flask-Bcrypt
- **数据库迁移**：Flask-Migrate
- **环境配置**：python-dotenv

## 安装指南

### 前提条件
- Python 3.7+ 
- pip 包管理器
- MySQL 或 SQLite 数据库

### 步骤 1: 克隆项目

```bash
# 克隆项目仓库
git clone https://your-repository-url/cyberpunk-blog.git
cd cyberpunk-blog
```

### 步骤 2: 创建虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤 4: 配置环境变量

复制 `.env.example` 文件并重命名为 `.env`，根据您的环境修改配置：

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

编辑 `.env` 文件，设置您的环境变量，特别是 `SECRET_KEY` 和 `DATABASE_URL`。

### 步骤 5: 初始化数据库

```bash
# 创建数据库表结构
flask db upgrade

# 或者运行初始化脚本
python init_db.py
```

### 步骤 6: 运行开发服务器

```bash
# 设置 Flask 应用
# Windows
sets FLASK_APP=app

sets FLASK_ENV=development

# macOS/Linux
export FLASK_APP=app
export FLASK_ENV=development

# 启动开发服务器
flask run
```

应用将在 http://127.0.0.1:5000/ 启动。

## 访问管理后台

打开浏览器，访问 http://127.0.0.1:5000/admin 进入管理后台。

默认管理员账号：
- 用户名: admin
- 密码: Admin123!

> **注意**：首次登录后请立即修改管理员密码。

## 目录结构

```
cyberpunk-blog/
├── app/
│   ├── __init__.py      # 应用初始化
│   ├── admin/           # 管理后台相关文件
│   │   └── templates/   # 管理后台模板
│   ├── forms/           # 表单定义
│   ├── models/          # 数据模型
│   ├── routes/          # 路由和视图函数
│   ├── static/          # 静态资源（CSS、JS、图片）
│   ├── templates/       # 前端模板
│   └── utils/           # 工具函数
├── config.py            # 应用配置
├── migrations/          # 数据库迁移文件
├── requirements.txt     # 项目依赖
└── tests/               # 测试代码
```

## 自定义赛博朋克风格

系统的赛博朋克风格设置可以在 `config.py` 文件中的 `CYBERPUNK_SETTINGS` 配置项中调整：

```python
CYBERPUNK_SETTINGS = {
    'theme': 'neon',
    'glitch_effect': True,
    'neon_colors': ['#00f0ff', '#ff00a0', '#00ff8c', '#fffc00']
}
```

## 部署到生产环境

在生产环境中，请确保：

1. 使用强密钥作为 `SECRET_KEY`
2. 设置 `DEBUG = False`
3. 启用 `SESSION_COOKIE_SECURE = True`
4. 使用生产级数据库（如 MySQL 或 PostgreSQL）
5. 配置 Web 服务器（如 Nginx）作为反向代理

## 许可证

[MIT License](LICENSE)

## 致谢

感谢所有为本项目做出贡献的开发者和设计师。