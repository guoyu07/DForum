# encoding=utf-8
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render
def index(request):
    return render(request,'topic/topics.html')

