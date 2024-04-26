from django.contrib import admin
from django.urls import path,include
from myApp import views


urlpatterns = [
    path('home', views.random, name="home"),
    path('', views.random, name="home"),
    path('all_emp/', views.all_emp, name="all_emp"),
    path('add_emp/', views.add_emp, name="add_emp"),
    path('remove_emp/', views.remove_emp, name="remove_emp"),
    path('remove_emp/<int:emp_id>', views.remove_emp, name="remove_emp"),
    path('change_emp/', views.change_emp, name='change_emp'),
    path('update_emp/', views.update_emp, name='update_emp'),
]