# coding=utf-8
from forum.models import User
def user_info(user):
    '''
        获得当前的用户信息
    '''
    counter = {
        'topics': user.topic_author.all().count(),
        'replies': user.reply_author.all().count(),
        'favorites': user.fav_user.all().count()
    }
    notifications_count = user.notify_user.filter(status=0).count()
    return counter, notifications_count


def update_reputation(uid, diff):
    '''
        更新声誉
    '''
    user = User.objects.get(pk=uid)
    user.reputation = user.reputation + diff
    user.save()
