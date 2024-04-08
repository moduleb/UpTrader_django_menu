from django.urls import path
from . import views

urlpatterns = [
    path('favicon.ico/', views.favicon, name='favicon'),

    path('', views.index, name='index'),
    path('<str:category>/', views.index, name='index'),
    path('<str:category>/<str:subcategory>/', views.index, name='index'),
    path('<str:category>/<str:subcategory>/<str:item>/', views.index, name='index'),
]

