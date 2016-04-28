# encoding=utf-8
from django.contrib.auth.models import AbstractUser
from django.db import models

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