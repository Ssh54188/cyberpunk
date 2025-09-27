from datetime import datetime, timedelta
import time

# 格式化日期时间
def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """将日期时间对象格式化为指定格式的字符串"""
    if not dt:
        return ''
    
    try:
        return dt.strftime(format_str)
    except Exception:
        return ''

def format_date(dt, format_str='%Y-%m-%d'):
    """将日期时间对象格式化为日期字符串"""
    return format_datetime(dt, format_str)

def format_time(dt, format_str='%H:%M:%S'):
    """将日期时间对象格式化为时间字符串"""
    return format_datetime(dt, format_str)

def time_ago(dt):
    """计算相对于当前时间的间隔，并返回人性化的时间描述"""
    if not dt:
        return ''
    
    now = datetime.utcnow()
    if dt.tzinfo:
        now = datetime.now(dt.tzinfo)
    
    # 计算时间差
    diff = now - dt
    
    # 转换为秒数
    seconds = diff.total_seconds()
    
    # 定义时间间隔对应的描述
    intervals = [
        (86400 * 365, '年'),
        (86400 * 30, '月'),
        (86400 * 7, '周'),
        (86400, '天'),
        (3600, '小时'),
        (60, '分钟'),
        (1, '秒')
    ]
    
    # 查找最合适的时间间隔
    for interval, unit in intervals:
        if seconds >= interval:
            count = int(seconds / interval)
            return f'{count}{unit}前'
    
    # 如果时间差小于1秒
    return '刚刚'

def parse_datetime(datetime_str, format_str='%Y-%m-%d %H:%M:%S'):
    """将字符串解析为日期时间对象"""
    if not datetime_str:
        return None
    
    try:
        return datetime.strptime(datetime_str, format_str)
    except ValueError:
        # 尝试其他常见格式
        try_formats = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M',
            '%d/%m/%Y'
        ]
        
        for fmt in try_formats:
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        
        return None

def get_current_timestamp():
    """获取当前时间的时间戳"""
    return int(time.time())

def get_datetime_from_timestamp(timestamp):
    """将时间戳转换为日期时间对象"""
    try:
        return datetime.fromtimestamp(timestamp)
    except (ValueError, TypeError):
        return None

def get_relative_month(months=0):
    """获取相对于当前时间的月份"""
    now = datetime.utcnow()
    year, month = divmod(now.month + months - 1, 12)
    return datetime(year + now.year, month + 1, 1)