# encoding=utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models
class Pages(object):
    '''
        分页查询类
    '''
    def __init__(self, count, current_page=1, list_rows=40):
        self.total = count
        self._current = current_page
        self.size = list_rows
        self.pages = self.total // self.size + (1 if self.total % self.size else 0)

        if (self.pages == 0) or (self._current < 1) or (self._current > self.pages):
            self.start = 0
            self.end = 0
            self.index = 1
        else:
            self.start = (self._current - 1) * self.size
            self.end = self.size + self.start
            self.index = self._current
        self.prev = self.index - 1 if self.index > 1 else self.index
        self.next = self.index + 1 if self.index < self.pages else self.index

class TopicManager(models.Manager):
    def get_all_topic(self, num=36, current_page=1): # 可以考虑在这里过滤掉没有头像的用户发帖，不显示在主页
        '''
            获得所有的topic
        '''
        count = self.get_queryset().count()
        page = Pages(count, current_page, num)
        query = self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            all().order_by('-last_touched', '-created', '-last_replied_time', '-id')[page.start:page.end]
        return query, page

    def get_topics_by_node(self,slug,current_page=1,num=20):
        '''
            根据帖子所在节点的slug获取所有的帖子
        '''
        count=self.get_queryset().filter(node__slug=slug).count()
        page=Pages(count,current_page,num)
        topics=self.get_queryset().select_related('node', 'author', 'last_replied_by')\
            .filter(node__slug=slug).order_by('-last_touched', '-created', '-last_replied_time', '-id')[page.start:page.end]
        return topics,page
    def get_topics_by_user(self,uid,current_page=1,num=20):
        '''
            根据用户获得所有的帖子
        '''
        count=self.get_queryset().filter(author__id=uid).count()
        page=Pages(count,current_page,num)
        topics=self.get_queryset().select_related('node', 'author', 'last_replied_by').\
            filter(author__id=uid).order_by('-id')[page.start:page.end]
        return topics,page
class NodeManager(models.Manager):
    def get_hot_node(self):
        pass

class NotiManager(models.Manager):
    def get_noti_by_user(self,uid,current_page=1,num=20):
        count=self.get_queryset().filter(involved_user__id=uid).count()
        page=Pages(count,current_page,num)
        notis=self.get_queryset().select_related('trigger_user', 'involved_topic')\
            .filter(involved_user__id=uid).order_by('-id')[page.start:page.end]
        return notis,page
class ReplyManager(models.Manager):
    '''
        获得所有的回复
    '''
    def get_all_replies(self,t_id,current_page=1,num=20):
        count=self.get_queryset().filter(topic__id=t_id).count()
        page=Pages(count,current_page,num)
        replies=self.get_queryset().select_related('author').filter(topic__id=t_id).order_by('id')[page.start:page.end]
        return replies,page

    def get_replies_by_user(self,uid,current_page=1,num=20):
        '''
            获得用户所有的回复
        '''
        count=self.get_queryset().filter(author__id=uid).count()
        page=Pages(count,current_page,num)
        replies=self.get_queryset().select_related('topic', 'topic__author'). \
                    filter(author__id=uid).order_by('-id')[page.start:page.end]
        return replies,page


class FavManager(models.Manager):
    def get_fav_by_user(self,uid,current_page=1,num=20):
        count=self.get_queryset().filter(owner_user__id=uid).count()
        page=Pages(count,current_page,num)
        favorites=self.get_queryset().select_related('involved_topic', 'involved_topic__node', \
                'involved_topic__author', 'involved_topic__last_replied_by') \
                .filter(owner_user__id=uid)[page.start:page.end]
        return favorites,page

class User(AbstractUser):
    '''
        定义一个User类，继承认证模块的抽象用户类，进行扩展
    '''

    nickname = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.CharField(max_length=200, null=True, blank=True)  # 头像
    about_me = models.CharField(max_length=500, null=True, blank=True)  # 关于我
    signature = models.CharField(max_length=500, null=True, blank=True)  # 签名
    location = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    role = models.IntegerField(null=True, blank=True)  # 角色
    balance = models.IntegerField(null=True, blank=True)  # 余额
    honor = models.IntegerField(null=True, blank=True)  # 荣誉
    updated = models.DateTimeField(null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    douban = models.CharField(max_length=200, null=True, blank=True)


class Plane(models.Model):
    '''
        论坛板块分类
    '''
    name = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)


class Node(models.Model):
    '''
        论坛板块
    '''
    name = models.CharField(max_length=200, null=True, blank=True)
    slug = models.CharField(max_length=200, null=True, blank=True)          # 板块的URL
    thumb = models.CharField(max_length=200, null=True, blank=True)         #
    introduction = models.CharField(max_length=500, null=True, blank=True)  # 节点介绍
    created = models.DateTimeField(null=True, blank=True) #创建时间
    updated = models.DateTimeField(null=True, blank=True) #更新时间
    plane = models.ForeignKey(Plane, null=True, blank=True) # 分类
    topic_count = models.IntegerField(null=True, blank=True) # 帖子数量
    custom_style = models.TextField(null=True, blank=True)
    limit_reputation = models.IntegerField(null=True, blank=True) # 最小声誉

    objects = NodeManager()


class Topic(models.Model):
    '''
        话题，论坛帖子的基本单位
    '''
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    node = models.ForeignKey(Node, null=True, blank=True)
    author = models.ForeignKey(User, related_name='topic_author', null=True, blank=True) # 设置了related_name后，可不用_set
    reply_count = models.IntegerField(null=True, blank=True)
    last_replied_by = models.ForeignKey(User, related_name='topic_last', null=True, blank=True)
    last_replied_time = models.DateTimeField(null=True, blank=True)
    up_vote = models.IntegerField(null=True, blank=True)
    down_vote = models.IntegerField(null=True, blank=True)
    last_touched = models.DateTimeField(null=True, blank=True)

    objects = TopicManager()

class Reply(models.Model):
    '''
        帖子的回复
    '''
    topic = models.ForeignKey(Topic, null=True, blank=True)
    author = models.ForeignKey(User, related_name='reply_author', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    up_vote = models.IntegerField(null=True, blank=True)
    down_vote = models.IntegerField(null=True, blank=True)
    last_touched = models.DateTimeField(null=True, blank=True)
    objects=ReplyManager()

class Favorite(models.Model):
    '''
        用户收藏的帖子或回复
    '''
    owner_user = models.ForeignKey(User, related_name='fav_user', null=True, blank=True)
    involved_type = models.IntegerField(null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='fav_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='fav_reply', null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    objects = FavManager()

class Notification(models.Model):
    '''
        站内通知
    '''
    content = models.TextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    involved_type = models.IntegerField(null=True, blank=True)
    involved_user = models.ForeignKey(User, related_name='notify_user', null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='notify_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='notify_reply', null=True, blank=True)
    trigger_user = models.ForeignKey(User, related_name='notify_trigger', null=True, blank=True)
    occurrence_time = models.DateTimeField(null=True, blank=True)
    objects = NotiManager()


class Vote(models.Model):
    '''
        投票
    '''
    status = models.IntegerField(null=True, blank=True)
    involved_type = models.IntegerField(null=True, blank=True)
    involved_user = models.ForeignKey(User, related_name='vote_user', null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='vote_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='vote_reply', null=True, blank=True)
    trigger_user = models.ForeignKey(User, related_name='vote_trigger', null=True, blank=True)
    occurrence_time = models.DateTimeField(null=True, blank=True)


class Transaction(models.Model):
    '''
        交易
    '''
    type = models.IntegerField(null=True, blank=True)
    reward = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, related_name='trans_user', null=True, blank=True)
    current_balance = models.IntegerField(null=True, blank=True)
    involved_user = models.ForeignKey(User, related_name='trans_involved', null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='trans_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='trans_reply', null=True, blank=True)
    occurrence_time = models.DateTimeField(null=True, blank=True)
