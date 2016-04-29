
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
    url(r'^admin/', admin.site.urls),
]
