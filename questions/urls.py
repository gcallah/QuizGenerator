from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses', views.courses, name='courses'),
    path('create_question', views.create_question, name='create_question'),
    path('courses/<str:course_id>/', views.course_details),
    path('courses/edit_course/<str:course_id>', views.edit_course, name='edit_course'),
    path('courses/<str:course_id>/edit_module', views.edit_module, name='edit_module'),
    path('delete_course/<str:course_id>', views.delete_course, name="delete_course"),
    path('login', views.login_request, name = 'login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_request, name = 'logout'),
    path('courses/<str:course_id>/create_module', views.create_module, name='create_module'),
    path('accounts/', include('django.contrib.auth.urls'))
]
