from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.user_auth, name='user_auth'),
    path('register/', views.createUser, name='createUser'),
    path('logout/', views.logout, name='logout')
]