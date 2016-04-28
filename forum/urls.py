
from django.conf.urls import url
from django.contrib import admin

from forum.views import topic
from forum.views import user
urlpatterns = [
    url(r'^$',topic.index,name='index'),
    url(r'^register/$',user.register,name='register'),
    url(r'^login/$',user.login,name='login'),
    url(r'^logout/$',user.logout,name='logout'),
    url(r'^admin/', admin.site.urls),
]
