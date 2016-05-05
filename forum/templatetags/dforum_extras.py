# encoding=utf-8

'''
自定义的过滤器
'''
from django import template
import random,re
from markdown import markdown
register=template.Library()
@register.filter
def pretty_date(time=None):
    return "2016-4-22"
@register.filter
def dump_errors(errors):
    t = template.Template('''
        {% if errors %}
        <ul class="errors alert alert-error">
            {% for v in errors.itervalues %}
                <li>{{ v | join:'，' }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        ''')
    c = template.Context(dict(errors=errors))
    return t.render(c)
@register.filter(name='markdown')
def markdown_up(content):
    if not content:
        return ''
    return markdown(content, extensions=['codehilite', 'fenced_code'], safe_mode='escape')
@register.filter
def content_process(content):
    '''
        内容过滤
    '''
    content = re.sub(r'http(s)?:\/\/gist.github.com\/(\d+)(.js)?',
                     r'<script src="http://gist.github.com/\2.js"></script>', content)
    # render sinaimg pictures
    content = re.sub(r'(http:\/\/\w+.sinaimg.cn\/.*?\.(jpg|gif|png))', r'<img src="\1" />', content)
    # render @ mention links
    content = re.sub(r'@(\w+)(\s|)', r'<a href="/u/\1/">@\1</a> ', content)
    # render youku videos
    content = re.sub(r'http://v.youku.com/v_show/id_(\w+).html',
                     r'<iframe height=498 width=510 src="http://player.youku.com/embed/\1" frameborder=0 allowfullscreen style="width:100%;max-width:510px;"></iframe>',
                     content)
    return content

@register.filter
def email_mosaic(email):
    if not email:
        return ''

    email_name = re.findall(r'^([^@]+)@', email)[0]

    if len(email_name) < 5:
        email_name = email_name + '***'
        email = re.sub(r'^([^@]+)@', '%s@' % email_name, email)
    else:
        email = re.sub(r'[^@]{3}@', '***@', email)

    return email
@register.simple_tag
def pagination(page, uri, list_rows = 10): # 显示分页
    def gen_page_list(current_page = 1, total_page = 1, list_rows = 10):
        if total_page <= list_rows:
            return range(1, total_page + 1)
        elif current_page <= (list_rows // 2):
            return range(1, list_rows + 1)
        elif current_page >= (total_page - list_rows // 2):
            return range(total_page - list_rows + 1, total_page + 1)
        else:
            return range(current_page - list_rows // 2, current_page - list_rows // 2 + list_rows)

    t = template.Template('''
        {% load dforum_extras %}
        {% if page and page.pages > 1 %}
            <ul>
                <li {% ifequal page.index page.prev %}class="disabled"{% endifequal %}><a href="{% build_uri uri 'p' page.prev %}">«</a></li>
                {% for p in gen_page_list %}
                    <li {% ifequal page.index p %}class="active"{% endifequal %}>
                        {% ifnotequal page.index p %}
                            <a href="{% build_uri uri 'p' p %}">{{ p }}</a>
                        {% else %}
                            <a href="javascript:;">{{ p }}</a>
                        {% endifnotequal %}
                    </li>
                {% endfor %}
                <li {% ifequal page.index page.next %}class="disabled"{% endifequal %}><a href="{% build_uri uri 'p' page.next %}">»</a></li>
            </ul>
        {% endif %}
        ''')
    c = template.Context(dict(page = page, uri = uri, gen_page_list = gen_page_list(page.index, page.pages, list_rows)))

    return t.render(c)

@register.simple_tag
def gen_random():
    return random.random()

@register.simple_tag
def build_uri(uri, param, value): # 给uri添加参数或者修改参数的值
    regx = re.compile('[\?&](%s=[^\?&]*)' % param)
    find = regx.search(uri)
    split = '&' if re.search(r'\?', uri) else '?'
    if not find: return '%s%s%s=%s' % (uri, split, param, value)
    return re.sub(find.group(1), '%s=%s' % (param, value), uri)