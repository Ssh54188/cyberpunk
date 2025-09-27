import markdown
from markdown.extensions import fenced_code, codehilite, tables, toc, nl2br
from markdown.extensions.wikilinks import WikiLinkExtension
from flask import Markup

# Markdown配置
def get_markdown_extensions():
    """获取Markdown扩展配置"""
    return [
        fenced_code.FencedCodeExtension(),  # 代码块支持
        codehilite.CodeHiliteExtension(css_class='highlight'),  # 代码高亮
        tables.TableExtension(),  # 表格支持
        toc.TocExtension(permalink=True),  # 目录支持
        nl2br.NL2BrExtension(),  # 换行转<br>
        WikiLinkExtension(base_url='/wiki/', end_url='')  # Wiki链接支持
    ]

def markdown_to_html(text, extensions=None):
    """将Markdown文本转换为HTML"""
    if not text:
        return ''
    
    # 如果没有提供扩展，使用默认扩展
    if extensions is None:
        extensions = get_markdown_extensions()
    
    # 转换Markdown为HTML
    html = markdown.markdown(text, extensions=extensions)
    
    # 返回安全的HTML（使用Flask的Markup类）
    return Markup(html)

def extract_markdown_title(text):
    """从Markdown文本中提取标题（第一个一级标题）"""
    if not text:
        return ''
    
    # 查找第一个一级标题
    import re
    match = re.search(r'^#\s+(.*)$', text, re.MULTILINE)
    if match:
        return match.group(1)
    
    return ''

def extract_markdown_excerpt(text, max_length=150):
    """从Markdown文本中提取摘要"""
    if not text:
        return ''
    
    # 移除Markdown标记
    # 这里使用简单的方法，实际应用中可能需要更复杂的处理
    from .text_processing import remove_html_tags, truncate_text
    
    # 首先转换为HTML，然后移除HTML标签
    html = markdown_to_html(text, extensions=[])
    plain_text = remove_html_tags(str(html))
    
    # 截断文本
    return truncate_text(plain_text, max_length)

def get_markdown_toc(text):
    """获取Markdown文档的目录"""
    if not text:
        return ''
    
    # 创建临时的Markdown转换器，仅用于生成目录
    md = markdown.Markdown(extensions=[toc.TocExtension(permalink=True)])
    md.convert(text)
    
    # 返回目录HTML
    return Markup(md.toc)