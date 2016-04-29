# coding: utf-8

import re
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def sendmail(title, content, to):
    msg = EmailMultiAlternatives(title, content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(content, 'text/html')
    msg.send()


def find_mentions(content):
    regex = re.compile(ur'@(?P<username>\w+)(\s|$)', re.I)
    return set([m.group('username') for m in regex.finditer(content)])