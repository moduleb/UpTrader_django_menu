from uuid import uuid4

from django.urls import path

from . import views
from .models import MenuItem

urlpatterns = [
    path('favicon.ico/', views.favicon, name='favicon'),
    path('', views.index, name='index'),
]

queryset = MenuItem.objects.all()

for item in queryset:

    if not item.url:
        url = str(uuid4())
    else:
        url = str(item.url).lstrip("/")

    urlpatterns.append(path(url, views.index, name=item.named_url))


"""
path('', views.index, name='index'),
path('<str:category>/', views.index, name='index'),
path('<str:category>/<str:subcategory>/', views.index, name='index'),
path('<str:category>/<str:subcategory>/<str:item>/', views.index, name='index'),
"""