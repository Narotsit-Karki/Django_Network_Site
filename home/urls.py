from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views
from .forms import UserLoginForm

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('signup',SignUpView.as_view(),name = 'sign-up'),

    path('login',views.LoginView.as_view(template_name = 'login.html',authentication_form = UserLoginForm))
]

