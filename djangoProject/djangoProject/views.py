from django.http import HttpResponse

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world!")


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")