import re
import unicodedata

# 生成URL友好的slug
def slugify(text, separator='-', max_length=200):
    """将文本转换为URL友好的slug格式"""
    # 标准化Unicode字符
    text = unicodedata.normalize('NFKD', text)
    # 转换为ASCII字符
    text = text.encode('ascii', 'ignore').decode('utf-8')
    # 转换为小写
    text = text.lower()
    # 移除非字母数字字符，保留空格
    text = re.sub(r'[^\w\s-]', '', text)
    # 将空格替换为分隔符
    text = re.sub(r'[\s-]+', separator, text)
    # 移除首尾的分隔符
    text = text.strip(separator)
    # 限制长度
    if len(text) > max_length:
        text = text[:max_length]
    # 确保结果不为空
    if not text:
        text = 'untitled'
    return text

def truncate_text(text, max_length=200, suffix='...'):
    """截断文本到指定长度，并添加后缀"""
    if not text:
        return ''
    
    # 如果文本长度小于等于最大长度，直接返回
    if len(text) <= max_length:
        return text
    
    # 截断文本
    truncated = text[:max_length]
    
    # 尝试在最近的空格处截断，以保持单词的完整性
    last_space = truncated.rfind(' ')
    if last_space > max_length * 0.7:  # 确保截断位置不会太靠近开头
        truncated = truncated[:last_space]
    
    return truncated + suffix

def remove_html_tags(text):
    """移除文本中的HTML标签"""
    if not text:
        return ''
    
    # 使用正则表达式移除HTML标签
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def count_words(text):
    """计算文本中的单词数量"""
    if not text:
        return 0
    
    # 移除HTML标签
    text = remove_html_tags(text)
    
    # 分割单词并计算数量
    words = text.split()
    return len(words)

def excerpt_from_content(content, max_length=150):
    """从文章内容中提取摘要"""
    if not content:
        return ''
    
    # 移除HTML标签
    text = remove_html_tags(content)
    
    # 截断文本
    return truncate_text(text, max_length)

def sanitize_filename(filename):
    """清理文件名，移除或替换不安全的字符"""
    if not filename:
        return ''
    
    # 保留文件名中的基本字符，替换其他字符为下划线
    # 保留字母、数字、点、下划线、连字符
    safe_chars = re.compile(r'[^a-zA-Z0-9._-]')
    return safe_chars.sub('_', filename)