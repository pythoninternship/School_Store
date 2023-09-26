from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('read_more/', views.read_view, name='read_view'),
    path('about/', views.about_view, name='about_view'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('logout', views.logout, name='logout'),
    path('login/?error=1', views.login_view, name='login_error'),
    path('order/', views.order_form_view, name='order_form_view'),
    path('get_courses/', views.get_courses, name='get_courses'),


]



