from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .views import BaseRegisterView
from .views import upgrade_me
from django.urls import include

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = 'sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    #path('signup/',
    #     BaseRegisterView.as_view(template_name = 'sign/signup.html'),
    #     name='signup'),

    path('signup/', views.register, name="register"),
    path('activation_code_form/', views.endreg, name="endreg"),

    #path('upgrade/', upgrade_me, name = 'upgrade'),
]