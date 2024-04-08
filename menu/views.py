from django.http import HttpResponse
from django.shortcuts import render


def favicon(request):
    return HttpResponse(status=204)


def index(request, **kwargs):
    return render(request, 'index.html', {"request": request})
