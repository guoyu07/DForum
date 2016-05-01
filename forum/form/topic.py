# coding=utf-8
from django import forms


class CreateForm(forms.Form):
    '''
        发帖表单
    '''
    title = forms.CharField(min_length=3, max_length=56,
                            error_messages={
                                'required': u'请填写帖子标题',
                                'min_length': u'帖子标题长度过短（3-56个字符）',
                                'max_length': u'帖子标题长度过长（3-56个字符）',})
    content = forms.CharField(min_length=15,
                              error_messages={
                                  'required': u'请填写帖子内容',
                                  'min_length': u'帖子内容长度过短（少于15个字符）',})

class ReplyForm(forms.Form):
    '''
        回复表单
    '''
    content=forms.CharField(min_length=5,error_messages={'required':u'请输入帖子内容',
                                                         'min_length':u'回复字数不能少于5'})

    def __init__(self,request):
        super(ReplyForm,self).__init__(request.POST)
        self.user=request.user
        self.reply_id=request.POST.get('rid')
    def clean(self):
        if self.user.id!=self.reply_id:
            raise forms.ValidationError(u'没有权限修改该回复')
        return self.cleaned_data