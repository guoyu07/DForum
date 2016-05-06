# coding=utf-8

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from forum.models import Notification
from tools import update_reputation,user_info
@login_required
def notifications(request):
    '''
        通知信息
    '''
    try:
        current_page=int(request.GET.get('p',1))
    except ValueError:
        current_page=1
    counter = user_info(request.user)[0]
    notifications,page=Notification.objects.get_noti_by_user(request.user.id,current_page)
    notifications_count=request.user.notify_user.filter(status=0).count()
    request.user.notify_user.filter(status=0).update(status=1)
    return render(request,'notifications/notifications.html',locals())

