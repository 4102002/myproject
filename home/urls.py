from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.login, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('get_file_description/', views.get_file_description, name='get_file_description'),
    path('loggedin', views.home, name='home'),
    path('register', views.signup, name='signup'),
    # path('send_mail', views.sendmail, name='home'),
]