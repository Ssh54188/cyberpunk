from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from app import db

class Setting(db.Model):
    """网站全局设置模型"""
    __tablename__ = 'settings'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = db.Column(db.String(50), unique=True, nullable=False, index=True)
    value = db.Column(db.Text)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), default='string', nullable=False)  # string, text, boolean, number, etc.
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __init__(self, key, value, **kwargs):
        """初始化设置对象"""
        self.key = key
        self.value = value
        
        # 设置其他可选字段
        for key_param, value_param in kwargs.items():
            if hasattr(self, key_param):
                setattr(self, key_param, value_param)
    
    def save(self):
        """保存设置到数据库"""
        db.session.add(self)
        db.session.commit()
    
    def update(self, **kwargs):
        """更新设置信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def delete(self):
        """从数据库删除设置"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_value(cls, key, default=None):
        """通过键获取设置值"""
        setting = cls.query.filter_by(key=key, is_active=True).first()
        if setting:
            # 根据类型转换值
            if setting.type == 'boolean':
                return setting.value.lower() == 'true'
            elif setting.type == 'number':
                try:
                    return int(setting.value)
                except ValueError:
                    try:
                        return float(setting.value)
                    except ValueError:
                        return setting.value
            return setting.value
        return default
    
    @classmethod
    def set_value(cls, key, value, description=None, setting_type='string'):
        """设置或更新一个设置项"""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
            if description:
                setting.description = description
            setting.type = setting_type
            db.session.commit()
        else:
            setting = cls(key=key, value=str(value), description=description, type=setting_type)
            setting.save()
    
    def __repr__(self):
        """返回设置的字符串表示"""
        return f'<Setting {self.key}>'