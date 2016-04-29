# encoding=utf-8
from forum.models import User,Node,Plane
from django.shortcuts import render
def index(request):
    user=request.user
    try:
        current_page=int(request.GET.get('p','1'))
    except ValueError:
        current_page=1
    hot_nodes=Node.objects.all()
    planes=Plane.objects.all().prefetch_related('node_set')
    return render(request,'topic/topics.html',locals())