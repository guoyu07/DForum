# coding=utf-8
from django.test import TestCase
from views.common import sendmail
# Create your tests here.

class EmailTest(TestCase):
    def test_emai(self):
        mail_title = u'前端社区（F2E.im）找回密码'
        var = {'email': "dd", 'new_password': 'dddddd'}
        sendmail(mail_title, 'content', 'cc959798@163.com')
