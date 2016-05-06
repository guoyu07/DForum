
from django.conf.urls import url
from django.contrib import admin

from forum.views import topic
from forum.views import user
from forum.views import notifications
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
    url(r'^t/edit/(\d+)/$',topic.topic_edit,name='edit'),
    url(r'^t/(\d+)/reply/$',topic.reply_create,name='reply_create'),
    url(r'^reply/edit/(\d+)/$',topic.reply_edit,name='reply_edit'),
    url(r'^node/(.*)/$',topic.node_topics,name='node_topics'),
    url(r'^u/(.*)/topics/$',topic.user_topics,name='user_topics'),
    url(r'^u/(.*)/replies/$',topic.user_replies,name='user_replies'),
    url(r'^u/(.*)/favorites/$',topic.favorite,name='favorites'),
    url(r'^u/(.*)/$',topic.profile,name='profile'),
    url(r'^favorite/$',topic.favorite_add,name='favorite_add'),
    url(r'^unfavorite/$',topic.favorite_del,name='favorite_del'),
    url(r'^members/$',topic.members,name='members'),
    url(r'^vote/$',topic.vote,name='vote'),
    url(r'^notifications/$',notifications.notifications,name='notifications'),
    url(r'^admin/', admin.site.urls),
]
