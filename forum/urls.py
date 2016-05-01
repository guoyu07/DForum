
from django.conf.urls import url
from django.contrib import admin

from forum.views import topic
from forum.views import user
urlpatterns = [
    url(r'^$',topic.index,name='index'),
    url(r'^register/$',user.register,name='register'),
    url(r'^login/$',user.login,name='login'),
    url(r'^logout/$',user.logout,name='logout'),
    url(r'^setting/$',user.setting,name='setting'),
    url(r'^setting/avatar/$',user.setting_avatar,name='setting_avatar'),
    url(r'^setting/password/$',user.seting_password,name='seeting_password'),
    url(r'^forgot/$',user.forgot,name='forgot'),
    url(r'^t/create/(.*)/$',topic.topic_create,name='topic_create'),
    # url(r'^t/(\d+)/$',topic.topic,name='topic'),
    url(r'^t/(\d+)/reply/$',topic.reply,name='reply'),
    url(r'^reply/edit/(\d+)/$',topic.reply_edit,name='reply_edit'),
    url(r'^admin/', admin.site.urls),
]
