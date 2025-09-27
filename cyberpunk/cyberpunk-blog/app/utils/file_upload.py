import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

# 允许上传的文件类型
def allowed_file(filename, allowed_extensions=None):
    """检查文件类型是否被允许上传"""
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'})
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def secure_filename_custom(filename):
    """生成安全的文件名，避免文件名冲突"""
    # 使用Werkzeug的secure_filename函数处理文件名
    safe_filename = secure_filename(filename)
    
    # 如果文件名被清空，使用随机名称
    if not safe_filename:
        safe_filename = str(uuid.uuid4())
    
    # 生成唯一的文件名，避免覆盖已存在的文件
    name, ext = os.path.splitext(safe_filename)
    unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
    
    return unique_filename

def save_file(file, upload_folder=None):
    """保存上传的文件并返回文件路径"""
    if upload_folder is None:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join('app', 'static', 'images', 'uploads'))
    
    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)
    
    # 生成安全的文件名
    filename = secure_filename_custom(file.filename)
    
    # 保存文件
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    # 返回相对路径（相对于项目根目录）
    relative_path = os.path.relpath(file_path, os.getcwd())
    return relative_path

def get_file_url(file_path):
    """获取文件的URL路径"""
    # 如果文件路径已经是URL，直接返回
    if file_path.startswith(('http://', 'https://')):
        return file_path
    
    # 否则，将文件路径转换为相对于static目录的URL
    static_path = os.path.join('app', 'static')
    if file_path.startswith(static_path):
        # 去除static目录前缀，得到相对路径
        rel_path = os.path.relpath(file_path, static_path)
        # 转换为URL路径（使用正斜杠）
        url_path = rel_path.replace(os.path.sep, '/')
        # 生成完整的URL路径
        return f"/static/{url_path}"
    
    return file_path

def delete_file(file_path):
    """删除指定的文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"删除文件失败: {e}")
        return False