from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.count_show, name='test_show'),
    path('movie/', views.dou_ban, name='movie')

]
