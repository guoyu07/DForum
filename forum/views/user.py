# encoding=utf-8
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from forum.form.user import RegisterForm,LoginForm

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
    print type(request)
    '''
        处理登陆请求
    '''
    if request.method=='GET':
        auth.logout(request)
        return render(request,'user/login.html')
    else:
        form=LoginForm(request.POST)
        if not form.is_valid():
            print form.errors
            return render(request,'user/login.html',form.errors)
        user=form.get_user()
        if user:
            auth.login(request,user)
        print user.is_staff
        if user.is_staff:
            return redirect(request.REQUEST.get('next', '/manage/admin/'))
        return redirect(reverse('forum:index'))

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next') or request.POST.get('next','/'))