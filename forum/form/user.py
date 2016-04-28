# coding=utf-8
from django import forms
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