# encoding=utf-8

'''
自定义的过滤器
'''
from django import template
import random
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
@register.simple_tag
def gen_random():
    return random.random()