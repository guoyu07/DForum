# encoding=utf-8

'''
自定义的过滤器
'''
from django import template
register=template.Library()
@register.filter
def pretty_date(time=None):
    return "2016-4-22"