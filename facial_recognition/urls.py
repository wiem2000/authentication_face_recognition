"""facial_recognition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from authentication_app.views import compare, index, login, video_feed
from user_authent_app.views import login_user, logout, password_reset, password_reset_confirm

from useradmin_app.views import delete_user, user_list, home2, update_mdp, update_user, user_info
from registration_app.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('', home2,name="home2"),
    
    path('user_list', user_list,name="user_list"),
    path('logout/',logout,name='logout'),
    path('login/',login,name="login"),
    
    
    path('index',index, name='index'),
    path('video_feed', video_feed, name='video_feed'),
    path('compare', compare, name='compare'),
    path('registration/',register,name='register'),
    
    path('login_user/<int:user_id>',login_user,name='login_user'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password-reset-confirm/<int:user_id>/', password_reset_confirm, name='password_reset_confirm'),

    path('user/<int:user_id>/',user_info,name='user_info'),
    path('update_user/<pk>',update_user,name='update_user'),
    path('update_mdp',update_mdp,name='update_mdp'),
    path('delete_user/<pk>',delete_user,name='delete_user'),

    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
