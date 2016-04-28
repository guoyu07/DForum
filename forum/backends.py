# encoding=utf-8

from django.contrib.auth.backends import ModelBackend
from models import User

class AuthBackend(ModelBackend):
    def authenticate(self,username=None,password=None):
        try:
            user=User.objects.filter(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None