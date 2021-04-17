from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.courses, name='courses'),
    path('courses/<str:course_id>/', views.course_details),
    path('delete_course/<str:course_id>', views.delete_course, name="delete_course"),
    path('login', views.login, name = 'login'),
    path('register', views.register, name='register'),
    path('courses/<str:course_id>/create_module', views.create_module, name='create_module')
]
