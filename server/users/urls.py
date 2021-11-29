from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('error_page/', views.error_dispose, name='error_dispose'),
    url(r'^captcha/', include('captcha.urls')),
    #静态页面URL
    path('', views.welcome_page, name='welcome_page'),
    path('index/', views.index_page, name='index_page'),
    path('base/', views.base_page, name='base'),
    path('register_page/', views.register_page, name='register_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout'),
    path('up_user_page/', views.up_user_page, name='up_user_page'),
    path('add_up_page/', views.add_up_user, name="add_up_page"),
    path('add_normal_page/', views.add_normal_user, name="add_normal_page"),
    path('max_critical/', views.evaluate, name="max_critical"),
    path('ping_feng_page/', views.ping_top, name="ping_feng_page"),
    path('analysis/', views.analysising, name="analysis"),
    path('tui_jian_page/', views.want_page, name="tui_jian_page"),
    path('movie_data_update/', views.data_update, name='data_page'),
    # 动态页面
    path('update_page/<str:pk>/', views.update_page, name='update_page'),
    path('change_page/<str:pk>/', views.change_password, name='change_password'),
    path('person_message/<str:pk>/', views.message_show, name='person_message'),
    path('delete_page/<str:pk>/', views.delete_page, name='delete_page'),
]
