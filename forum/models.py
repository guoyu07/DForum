# encoding=utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models

class TopicManager(models.Manager):
    pass
class NodeManager(models.Manager):
    def get_hot_node(self):
        pass

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

