# coding=utf-8
from django import forms
from django.contrib.auth import authenticate
from forum.models import User
from DForum import settings
error_message={
    'username': {
        'required': u'请填写用户名',
        'min_length': u'用户名长度不合法（6-12个字符）',
        'max_length': u'用户名长度不合法（6-12个字符）',
        'invalid': u'用户名格式错误（英文字母开头，数字，下划线构成）'
    },
    'email': {
        'required': u'必须填写email',
        'min_length': u'email长度有误',
        'max_length': u'email长度有误',
        'invalid': u'email地址无效'
    },
    'password': {
        'required': u'请填写密码',
        'min_length': u'密码长度过短（6-64个字符）',
        'max_length': u'密码长度过长（6-64个字符）'
    },
    'password_confirm':{
        'required': u'请填写确认密码',
        'min_length': u'密码长度过短（6-64个字符）',
        'max_length': u'密码长度过长（6-64个字符）'
    }
}


class RegisterForm(forms.ModelForm):
    '''
        注册表单
    '''
    username=forms.RegexField(min_length=6,max_length=12,
                              regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',error_messages=error_message['username'])
    email=forms.EmailField(min_length=4,max_length=64,
                           error_messages=error_message['email'])
    password=forms.CharField(min_length=6,max_length=64,widget=forms.PasswordInput,
                               error_messages=error_message['password'])
    password_confirm=forms.CharField(min_length=6, max_length=64, widget=forms.PasswordInput,
                                         error_messages=error_message['password_confirm'])

    class Meta:
        model=User
        fields=('username','email')
    def clean_username(self):
        username=self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u'用户名已存在')
        except User.DoesNotExist:
            if username in settings.RESERVED:
                raise forms.ValidationError(u'用户名不合法')
            return username

    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(u'邮箱已经被注册')
        except User.DoesNotExist:
            return email
    def clean_password_confirm(self):
        password1=self.cleaned_data['password']
        password2=self.cleaned_data['password_confirm']
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError(u'两次密码不一致')
    def save(self,commit=True):
        user=super(RegisterForm,self).save()
        user.set_password(self.cleaned_data['password'])
        if user:
            user.save()
        return user

class LoginForm(forms.Form):
    '''
        登陆表单
    '''
    email=forms.EmailField(min_length=4,max_length=64,
                          error_messages=error_message['email'])
    password=forms.CharField(min_length=6,max_length=64,
                             error_messages=error_message['password'],
                             widget=forms.PasswordInput)
    def clean(self):
        email=self.cleaned_data['email']
        password=self.cleaned_data['password']
        if email and password:
            self.user=authenticate(username=email,password=password)
            if not self.user:
                raise forms.ValidationError(u'用户名或密码错误')
            elif not self.user.is_active:
                raise forms.ValidationError(u'你的账户被锁定,请联系管理员')
        return self.cleaned_data
    def get_user(self):
        return self.user
class SettingForm(forms.Form):
    '''
        用户设置表单
    '''
    username = forms.CharField() # 不能修改
    email = forms.EmailField() # 不能修改
    nickname = forms.CharField(min_length=3, max_length=12, required=False,
        error_messages={
            'min_length': u'昵称长度过短（3-12个字符）',
            'max_length': u'昵称长度过长（3-12个字符）',
        })
    signature = forms.CharField(required=False)
    location = forms.CharField(required=False)
    website = forms.URLField(required=False,
        error_messages={
            'invalid': u'请填写合法的URL地址）',
        })
    company = forms.CharField(required=False)
    github = forms.CharField(required=False)
    twitter = forms.CharField(required=False)
    douban = forms.CharField(required=False)
    self_intro = forms.CharField(required=False)

class SettingPassForm(forms.Form):
    password_old=forms.CharField(min_length=6,max_length=12,widget=forms.PasswordInput,
                                 error_messages=error_message['password'])
    password=forms.CharField(min_length=6,max_length=12,widget=forms.PasswordInput,
                             error_messages=error_message['password'])
    password_confirm=forms.CharField(min_length=6,max_length=12,widget=forms.PasswordInput,
                                     error_messages=error_message['password_confirm'])
    def __init__(self,request):
        self.user=request.user
        super(SettingPassForm,self).__init__(request.POST)
    def clean(self):
        passwrod_old=self.cleaned_data['password_old']
        passwrod=self.cleaned_data['password']
        passwrod_confirm=self.cleaned_data['password_confirm']
        if not (passwrod_old and self.user.check_password(passwrod_old)):
            raise forms.ValidationError(u'旧密码错误')
        if passwrod!=passwrod_confirm:
            return forms.ValidationError(u'两次密码不一致')
        return self.cleaned_data

class ForgotForm(forms.Form):
    '''
        忘记密码表单
    '''
    username=forms.CharField(min_length=6,max_length=64,
                             error_messages=error_message['username'])
    email=forms.CharField(min_length=6,max_length=64,
                          error_messages=error_message['email'])
    def clean(self):
        username=self.cleaned_data['username']
        email=self.cleaned_data['email']
        if username and email:
            try:
                self.user=User.objects.get(email=email,username=username)
            except User.DoesNotExist:
                raise forms.ValidationError(u'用户名或者邮箱错误')
        return self.cleaned_data
    def get_user(self):
        return self.user

