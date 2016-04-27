
from django.conf.urls import url
from django.contrib import admin

from forum.views import topic

urlpatterns = [
    url(r'^$',topic.get_index),
    url(r'^admin/', admin.site.urls),
]
