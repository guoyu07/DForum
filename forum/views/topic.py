# encoding=utf-8
from forum.models import User, Node, Plane,Topic,Reply
from django.http import Http404
from django.shortcuts import render, get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from forum.form.topic import CreateForm,ReplyForm


def index(request):
    user = request.user
    if user.is_authenticated():
        counter = {
            'topics': user.topic_author.all().count(),
            # 'replies': user.reply_author.all().count(),
            # 'favorites': user.fav_user.all().count()
        }
    try:
        current_page = int(request.GET.get('p', '1'))
    except ValueError:
        current_page = 1
    status_counter = {
        'users': User.objects.all().count(),
        'nodes': Node.objects.all().count(),
        'topics': Topic.objects.all().count(),
        # 'replies': Reply.objects.all().count(),
    }
    hot_nodes = Node.objects.all()
    topics,topic_page=Topic.objects.get_all_topic(current_page=current_page)
    planes = Plane.objects.all().prefetch_related('node_set')
    return render(request, 'topic/topics.html', locals())


@login_required
def topic_create(request, slug):
    '''
        发表新帖子
    '''
    node = get_object_or_404(Node, slug=slug)
    form=CreateForm()
    if request.method=="POST":
        form=CreateForm(request.POST)
        if form.is_valid():
            user=request.user
            topic=Topic(title=form.cleaned_data['title'],
                        content=form.cleaned_data['content'],
                        created=timezone.now(),
                        node=node,
                        author=user,
                        reply_count=0,
                        last_touched=timezone.now())
            topic.save()
            return redirect(reverse('forum:index'))
    user = request.user
    #发帖查重
    counter = {
        'topics': user.topic_author.all().count(),
        # 'replies':user.reply_author.all().count(),
        'favorites': user.topic_last.all().count()
    }
    active_page = 'topic'
    node_slug = node.slug
    #User的声誉
    return render(request, 'topic/create.html', locals())

def reply(request,t_id):
    '''
        创建回复
    '''
    if request.method=="POST":
        try:
            topic=Topic.objects.select_related('author').get(pk=t_id)
        except Topic.DoesNotExist:
            return Http404
        form=ReplyForm(request.POST)
        if form.is_valid():
            user=request.user
            #回复重复验证

            now=timezone.now()
            reply=Reply(topic=topic,
                        author=user,
                        content=form.cleaned_data['content'],
                        created=now)
            reply.save()
            Topic.objects.filter(pk=t_id).update(last_replied_by=user,last_replied_time=now,
                                                 last_touched=now,reply_count=topic.reply_count+1)
            return redirect(reverse('forum:reply',args=[t_id])+'#reply'+str(topic.reply_count+1))

    topic = Topic.objects.get(pk=t_id)
    reply_last_page = (topic.reply_count // 20 + (topic.reply_count % 20 and 1)) or 1
    try:
        current_page = int(request.GET.get('p', reply_last_page))
    except ValueError:
        current_page = reply_last_page
    replies, reply_page = Reply.objects.get_all_replies(t_id, current_page, 20)
    return render(request, 'topic/view.html', locals())
@login_required
def reply_edit(request,id):
    print request.POST
    reply=get_object_or_404(Reply,pk=id)
    user=request.user
    if request.method=="POST":
        form=ReplyForm(request)
        if form.is_valid():
            if user.id==reply.author_id:
                Reply.objects.filter(pk=reply.id).update(updated=timezone.now(), content=form.cleaned_data['content'])
                return redirect(reverse('forum:reply',args=[reply.topic.id]))
    counter = {
        'topics': user.topic_author.all().count(),
        'replies': user.reply_author.all().count(),
        # 'favorites': user.fav_user.all().count()
    }
    # active_page='topic'
    return  render(request,'topic/reply_edit.html',locals())


