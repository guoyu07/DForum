# encoding=utf-8
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render
def get_index(request):
    
    return render(request,'topic/topics.html')
    return HttpResponse('<h1>hello world</h1>')