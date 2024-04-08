from django.http import HttpResponse
from django.shortcuts import render


def favicon(request):
    # Возвращаем пустой ответ с кодом 204 (No Content)
    return HttpResponse(status=204)

def index(request):
    context = {
        'request': request
    }
    return render(request, 'index.html', context)

def product_detail(request, animal, subcategory, product):
    context = {
        'animal': animal,
        'subcategory': subcategory,
        'product': product,
        'request': request
    }
    return render(request, 'index.html', context)

def category(request, animal, category):
    context = {
        'category': category,
        'animal': animal,
        'request': request
    }
    return render(request, 'index.html', context)

def animal(request, animal):
    context = {
        'animal': animal,
        'request': request
    }
    return render(request, 'index.html', context)