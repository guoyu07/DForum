# encoding=utf-8
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout,login
from forum.form.user import RegisterForm

def register(request):
    '''
        处理注册请求
    '''
    if request.method=='GET':
        logout(request)
        return render(request,'user/register.html')
    else:
        form=RegisterForm(request.POST)
        if not form.is_valid():
            print form.errors
            return render(request, 'user/register.html')
        user=form.save()
        if user:
            #发送邮件
            pass
        return redirect(reverse('forum:login'))

def login(request):
    if request.method=='GET':
        return render(request,'user/login.html')
    else:
        pass