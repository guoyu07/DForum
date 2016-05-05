# coding=utf-8
from django.core.urlresolvers import reverse
def custom_proc(request):
    return dict(
        navigation_bar = [
            (reverse('forum:index'), 'topic', '社区'),
            (reverse('forum:members'), 'members', '成员'),
            ('/static/pages/timeline/index.html', 'timeline', '大事记'),
            ('/static/pages/nav/index.html', 'nav', '导航'),
        ],
    )
