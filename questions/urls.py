from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.courses, name='courses'),
    path('courses/<str:course_id>/', views.course_details),
    path('register', views.register, name='register')
    
]
