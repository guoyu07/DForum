# encoding=utf-8
from forum.models import User, Node, Plane, Topic, Reply, Favorite, Notification, Vote
from forum.form.topic import CreateForm, ReplyForm
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from common import find_mentions
import json


def index(request):
    user = request.user
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    status_counter = {
        'users': User.objects.all().count(),
        'nodes': Node.objects.all().count(),
        'topics': Topic.objects.all().count(),
        'replies': Reply.objects.all().count(),
    }
    try:
        current_page = int(request.GET.get('p', '1'))
    except ValueError:
        current_page = 1
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    hot_nodes = Node.objects.all()
    topics, topic_page = Topic.objects.get_all_topic(current_page=current_page)
    planes = Plane.objects.all().prefetch_related('node_set')
    active_page = 'topic'
    return render(request, 'topic/topics.html', locals())


@login_required
def topic_create(request, slug):
    '''
        发表新帖子
    '''
    node = get_object_or_404(Node, slug=slug)
    form = CreateForm()
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            user = request.user
            topic = Topic(title=form.cleaned_data['title'],
                          content=form.cleaned_data['content'],
                          created=timezone.now(),
                          node=node,
                          author=user,
                          reply_count=0,
                          last_touched=timezone.now())
            topic.save()
            return redirect(reverse('forum:index'))
    user = request.user
    # 发帖查重
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    active_page = 'topic'
    node_slug = node.slug
    update_reputation(user.id, -5)
    return render(request, 'topic/create.html', locals())


def reply_create(request, t_id):
    '''
        创建回复
    '''
    if request.method == "POST":
        if not request.user.is_authenticated():
            return redirect(reverse('forum:login'))
        try:
            topic = Topic.objects.select_related('author').get(pk=t_id)
        except Topic.DoesNotExist:
            return Http404
        form = ReplyForm(request.POST)
        if form.is_valid():
            user = request.user
            reply = Reply(content=form.cleaned_data['content'],
                          created=timezone.now(),
                          author=user,
                          topic=topic,
                          last_touched=timezone.now())
            reply.save()
            return redirect(reverse('forum:reply_create', args=[topic.id]) + '#reply' + str(topic.reply_count + 1))
    user = request.user

    topic = Topic.objects.get(pk=t_id)
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
        topic_favorited = Favorite.objects.filter(involved_topic=topic, owner_user=user).exists()
    reply_last_page = (topic.reply_count // 20 + (topic.reply_count % 20 and 1)) or 1
    try:
        current_page = int(request.GET.get('p', reply_last_page))
    except ValueError:
        current_page = reply_last_page
    replies, reply_page = Reply.objects.get_all_replies(t_id, current_page, 20)
    return render(request, 'topic/view.html', locals())


@login_required
def reply_edit(request, id):
    '''
        用户回复修改
    '''
    reply = get_object_or_404(Reply, pk=id)
    user = request.user
    if request.method == "POST":
        if user.id == reply.author_id:
            form = ReplyForm(request.POST)
            if form.is_valid():
                if user.id == reply.author_id:
                    Reply.objects.filter(pk=reply.id).update(updated=timezone.now(),
                                                             content=form.cleaned_data['content'])
                    return redirect(reverse('forum:reply', args=[reply.topic.id]))
        else:
            errors = {'invalid_permission': [u'没有权限修改该回复']}
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    update_reputation(user.id, -2)
    active_page = 'topic'
    return render(request, 'topic/reply_edit.html', locals())


@login_required
def topic_edit(request, t_id):
    topic = get_object_or_404(Topic, pk=t_id)
    user = request.user
    if request.method == "POST":
        if user.id == topic.author_id:
            form = CreateForm(request.POST)
            if form.is_valid():
                user = request.user
                topic.title = form.cleaned_data['title']
                topic.content = form.cleaned_data['content']
                topic.save()
                return redirect(reverse('forum:index'))
        else:
            errors = {'invalid_permission': [u'没有权限修改该回复']}
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    update_reputation(user.id, -2)
    return render(request, 'topic/edit.html', locals())


def node_topics(request, slug):
    '''
        根据节点获得帖子
    '''
    node = get_object_or_404(Node, slug=slug)
    user = request.user
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
        # noti
    try:
        current_page = int(request.GET.get('p', 1))
    except ValueError:
        current_page = 1
    topics, topic_page = Topic.objects.get_topics_by_node(slug=slug, current_page=current_page)
    active_page = 'topic'
    return render(request, 'topic/node_topics.html', locals())


def user_topics(request, uid):
    '''
        根据用户获得帖子
    '''
    if uid.isdigit():
        user = get_object_or_404(User, pk=uid)
    else:
        user = get_object_or_404(User, username=uid)

    try:
        current_page = int(request.GET.get('p', 1))
    except ValueError:
        current_page = 1
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
        # noti

    topics, topic_page = Topic.objects.get_topics_by_user(user.id, current_page=current_page)
    active_page = 'topic'
    return render(request, 'topic/user_topics.html', locals())


def user_replies(request, uid):
    '''
        根据用户获得回复
    '''
    if uid.isdigit():
        user = get_object_or_404(User, pk=uid)
    else:
        user = get_object_or_404(User, username=uid)
    try:
        current_page = int(request.GET.get('p', 1))
    except ValueError:
        current_page = 1
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    replies, reply_page = Reply.objects.get_replies_by_user(user.id, current_page=current_page)
    active_page = 'topic'
    return render(request, 'topic/user_replies.html', locals())


def profile(request, uid):
    '''
        获得用户描述信息
    '''
    if uid.isdigit():
        user = get_object_or_404(User, pk=uid)
    else:
        user = get_object_or_404(User, username=uid)

    try:
        current_page = int(request.GET.get('p', 1))
    except ValueError:
        current_page = 1
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    topics, topic_page = Topic.objects.get_topics_by_user(user.id, current_page=current_page)
    replies, reply_page = Reply.objects.get_replies_by_user(user.id, current_page=current_page)
    active_page = '_blank'
    return render(request, 'topic/profile.html', locals())


def favorite(request, uid):
    if uid.isdigit():
        user = get_object_or_404(User, pk=uid)
    else:
        user = get_object_or_404(User, username=uid)

    try:
        current_page = int(request.GET.get('p', 1))
    except ValueError:
        current_page = 1
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    favorites, page = Favorite.objects.get_fav_by_user(user.id, current_page)
    return render(request, 'topic/user_favorites.html', locals())


def favorite_add(request):
    '''
        添加收藏
    '''
    msg = {'success': 0,
           'message': ''}
    user = request.user
    if not user.is_authenticated():
        msg['message'] = 'user_not_login'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    try:
        topic_id = int(request.GET.get('topic_id'))
    except ValueError:
        topic_id = Node
    if topic_id:
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            pass
    if not (topic_id and topic):
        msg['message'] = 'topic_not_exist'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    if user.id == topic.author_id:
        msg['message'] = "can_not_favorite_your_topic"
        return HttpResponse(json.dumps(msg), content_type='application/json')
    if Favorite.objects.filter(owner_user=user, involved_topic=topic).exists():
        msg['message'] = 'already_favorited'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    update_reputation(topic.author_id, 2)
    fav = Favorite(owner_user=user, involved_type=0, involved_topic=topic, created=timezone.now())
    fav.save()
    msg['message'] = 'save_favorite_success'
    msg['success'] = 1
    return HttpResponse(json.dumps(msg), content_type='application/json')


def favorite_del(request):
    '''
        删除收藏
    '''
    msg = {'success': 0,
           'message': ''}
    user = request.user
    try:
        topic_id = int(request.GET.get('topic_id'))
    except ValueError:
        topic_id = None
    if topic_id:
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            pass
    if not (topic_id and topic):
        msg['message'] = 'topic_not_exist'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    try:
        fav = Favorite.objects.get(owner_user=user, involved_topic=topic)
    except Favorite.DoesNotExist:
        fav = None

    if not fav:
        msg['message'] = 'not_been_favorited'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    update_reputation(topic.author_id, -2)
    fav.delete()
    msg['message'] = 'cancel_favorite_success'
    msg['success'] = 1
    return HttpResponse(json.dumps(msg), content_type='application/json')


def vote(request):
    '''
        点击喜欢
    '''
    msg = {'success': 0,
           'message': ''}
    user = request.user
    if not user.is_authenticated():
        msg['message'] = 'user_not_login'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    try:
        topic_id = int(request.GET.get('topic_id'))
    except ValueError:
        topic_id = Node
    if topic_id:
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            pass
    if not (topic_id and topic):
        msg['message'] = 'topic_not_exist'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    if user.id == topic.author_id:
        msg['message'] = "can_not_vote_your_topic"
        return HttpResponse(json.dumps(msg), content_type='application/json')
    if Vote.objects.filter(trigger_user=user, involved_topic=topic).exists():
        msg['message'] = 'already_voted'
        return HttpResponse(json.dumps(msg), content_type='application/json')
    # 声誉

    vote = Vote(trigger_user=user, involved_type=0, involved_topic=topic,
                involved_user=topic.author, status=0, occurrence_time=timezone.now())
    vote.save()
    msg['message'] = 'thanks_for_your_vote'
    msg['success'] = 1
    return HttpResponse(json.dumps(msg), content_type='application/json')


def members(request):
    '''
        获得所有的成员信息
    '''
    if request.user.is_authenticated():
        counter, notifications_count = user_info(request)
    members = User.objects.all().order_by('-id')[:49]
    active_members = User.objects.all().order_by('-last_login')[:49]
    active_page = 'members'
    return render(request, 'topic/members.html', locals())


def user_info(request):
    '''
        获得当前的用户信息
    '''
    user = request.user
    if user.is_authenticated():
        counter = {
            'topics': user.topic_author.all().count(),
            'replies': user.reply_author.all().count(),
            'favorites': user.fav_user.all().count()
        }
        notifications_count = user.notify_user.filter(status=0).count()
        return counter, notifications_count


def update_reputation(uid, diff):
    '''
        更新声誉
    '''
    user = User.objects.get(pk=uid)
    user.reputation = user.reputation + diff
    user.save()
