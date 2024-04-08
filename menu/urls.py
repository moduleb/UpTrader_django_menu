from django.urls import path
from . import views

urlpatterns = [
    path('favicon.ico/', views.favicon, name='favicon'),
    path('<str:animal>/<str:subcategory>/<str:product>/', views.product_detail, name='product_detail'),
    path('<str:animal>/<str:category>/', views.category, name='category'),
    path('<str:animal>/', views.animal, name='animal'),
    path('', views.index, name='index'),
]

