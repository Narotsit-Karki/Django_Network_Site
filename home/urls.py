from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views
from .forms import UserLoginForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',HomeView.as_view(),name = 'home'),
    path('signup',SignUpView.as_view(),name = 'sign-up'),
    path('login',views.LoginView.as_view(template_name = 'login.html',authentication_form = UserLoginForm)),
    path('profile/<username>',ProfileView.as_view(),name='profile'),
    path('follow-unfollow-user/<username>',follow_unfollow_user,name = 'follow'),

]

# creating image url
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)