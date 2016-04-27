from django.http import HttpResponse

def handler404(request):
    return HttpResponse('<h1>404</h1>')
def handler500(request):
    return HttpResponse("<h1>500</h1>")