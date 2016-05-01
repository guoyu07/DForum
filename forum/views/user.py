# encoding=utf-8
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.template import loader,Context
from django.utils import timezone
from forum.form.user import RegisterForm,LoginForm,SettingForm,SettingPassForm,ForgotForm
from PIL import Image
from common import sendmail
import copy,uuid,os

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
            return render(request, 'user/register.html',locals())
        user=form.save()
        if user:
            #发送邮件
            mail_title = u'DForum社区注册成功通知'
            mail_content = loader.get_template('user/register_mail.html').render(Context({}))
            sendmail(mail_title, mail_content, user.email)
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
            return render(request,'user/login.html',{'errors':form.errors})
        user=form.get_user()
        if user:
            auth.login(request,user)
        print user.is_staff
        if user.is_staff:
            return redirect(request.POST.get('next') or request.GET.get('next', '/'))
        return redirect(reverse('forum:index'))

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('next') or request.POST.get('next','/'))

@login_required
def setting(request):
    '''
        处理用户设置请求
    '''
    if request.method=="GET":
        return render(request,'user/setting.html')
    else:
        form=SettingForm(request.POST)
        if not form.is_valid():
            return render(request,'user/setting.html',{'errors':form.errors})
        user=request.user
        cp=copy.copy(form.cleaned_data)
        cp.pop('username')
        cp.pop('email')
        for k,v in cp.items():
            setattr(user,k,v)
        user.updated=timezone.now()
        user.save()
        messages.add_message(request,messages.SUCCESS,u'用户资料在更成功')
        return render(request,'user/setting.html',{'success_message':u'用户资料在更成功'})

@login_required
def setting_avatar(request):
    '''
        头像处理
    '''
    if request.method=="GET":
        return render(request,'user/setting_avatar.html')
    else:
        if not 'avatar' in request.FILES:
            return render(request,'user/setting_avatar.html',
                          errors={'invalid_avatar': [u'请先选择要上传的头像'],})
        user = request.user
        avatar_name = '%s' % uuid.uuid5(uuid.NAMESPACE_DNS, str(user.id))
        avatar = Image.open(request.FILES['avatar'])

        # crop avatar if it's not square
        avatar_w, avatar_h = avatar.size
        avatar_border = avatar_w if avatar_w < avatar_h else avatar_h
        avatar_crop_region = (0, 0, avatar_border, avatar_border)
        avatar = avatar.crop(avatar_crop_region)

        avatar_96x96 = avatar.resize((96, 96), Image.ANTIALIAS)
        avatar_48x48 = avatar.resize((48, 48), Image.ANTIALIAS)
        avatar_32x32 = avatar.resize((32, 32), Image.ANTIALIAS)
        path = os.path.dirname(__file__)
        avatar_96x96.save(os.path.join(path, '../static/avatar/b_%s.png' % avatar_name), 'PNG')
        avatar_48x48.save(os.path.join(path, '../static/avatar/m_%s.png' % avatar_name), 'PNG')
        avatar_32x32.save(os.path.join(path, '../static/avatar/s_%s.png' % avatar_name), 'PNG')
        user.avatar = '%s.png' % avatar_name
        user.updated = timezone.now()
        user.save()
        return render(request,'user/setting_avatar.html')

@login_required
def seting_password(request):
    '''
        重设密码
    '''
    print request.POST
    if request.method=="GET":
        return render(request,'user/setting_password.html')
    else:
        form=SettingPassForm(request)
        if not form.is_valid():
            return render(request, 'user/setting_password.html',{'errors':form.errors})
        user=request.user
        user.set_password(form.cleaned_data['password'])
        user.updated=timezone.now()
        user.save()
        return render(request,'user/setting_password.html',{'success_message':u'更新密码成功'})

def forgot(request):
    '''
        处理忘记密码
    '''
    if request.method=="GET":
        return render(request,'user/forgot.html')
    else:
        form=ForgotForm(request.POST)
        if not form.is_valid():
            print form.errors
            return render(request,'user/forgot.html',{'errors':form.errors})
        user=form.get_user()
        password=uuid.uuid1().hex
        user.set_password(password)
        user.save()
        title='dforum找回密码'
        content=render(None,'user/forgot_password_mail.html',{"email":user.email,'new_password':password})
        content=loader.get_template('user/forgot_password_mail.html').render(Context({"email":user.email,'new_password':password}))
        print type(content)
        sendmail(title,content,user.email)
        return render(request, 'user/forgot.html', {'success_message': u'新的密码已经发送到你的邮箱中'})

