import os
import hashlib
import hmac
import base64
import jwt
from datetime import datetime, timedelta
from flask import current_app, request

# 密码加密和验证
def hash_password(password, salt=None):
    """使用PBKDF2算法加密密码"""
    if salt is None:
        salt = os.urandom(32)
    elif isinstance(salt, str):
        salt = salt.encode('utf-8')
    
    # 使用Flask的bcrypt扩展处理密码加密
    from app import bcrypt
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, password):
    """验证密码是否正确"""
    # 使用Flask的bcrypt扩展验证密码
    from app import bcrypt
    return bcrypt.check_password_hash(hashed_password, password)

# 生成和验证JWT令牌
def generate_token(user_id, expires_in=3600):
    """生成JWT令牌"""
    secret_key = current_app.config.get('SECRET_KEY', 'default-secret-key')
    
    # 设置令牌的过期时间
    exp = datetime.utcnow() + timedelta(seconds=expires_in)
    
    # 创建令牌数据
    payload = {
        'sub': user_id,  # 主题，通常是用户ID
        'iat': datetime.utcnow(),  # 签发时间
        'exp': exp  # 过期时间
    }
    
    # 生成令牌
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    # 确保返回的是字符串
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    
    return token

def verify_token(token):
    """验证JWT令牌并返回用户ID"""
    secret_key = current_app.config.get('SECRET_KEY', 'default-secret-key')
    
    try:
        # 解码令牌
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # 返回用户ID
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        # 令牌已过期
        return None
    except jwt.InvalidTokenError:
        # 令牌无效
        return None

def generate_csrf_token():
    """生成CSRF令牌"""
    # Flask-WTF已经内置了CSRF保护功能
    # 这里提供一个简单的CSRF令牌生成函数作为备用
    if 'csrf_token' not in current_app.config:
        current_app.config['csrf_token'] = base64.b64encode(os.urandom(32)).decode('utf-8')
    
    return current_app.config['csrf_token']

def verify_csrf_token(token):
    """验证CSRF令牌"""
    if 'csrf_token' not in current_app.config:
        return False
    
    return hmac.compare_digest(current_app.config['csrf_token'], token)

def get_client_ip():
    """获取客户端的IP地址"""
    # 检查是否存在代理服务器
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    else:
        ip = request.remote_addr
    
    return ip

def is_safe_url(target):
    """检查URL是否安全（防止开放重定向攻击）"""
    from urllib.parse import urlparse, urljoin
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    
    # 确保目标URL的主机名与当前主机名相同
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def sanitize_input(input_string):
    """清理用户输入，防止XSS攻击"""
    if not input_string:
        return ''
    
    # 移除或替换可能导致XSS攻击的字符
    # 这里使用简单的替换，实际应用中可能需要使用更复杂的HTML清理库
    import html
    return html.escape(input_string)