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
    path('profile/<username>/about',AboutView.as_view(),name = 'profile-about'),
    path('profile/<username>/saved',SavedView.as_view(), name = 'profile-saved'),
    path('profile/<username>/friends',FriendView.as_view(), name = 'profile-friends'),
    path('profile/<username>/photos',PhotosView.as_view(),name = 'profile-photos'),
    path('profile/<username>/update-background',update_background, name = 'profile-update-background'),
    path('profile/<username>/update-profile',update_profile_pic,name = 'profile-update-pp'),

    path('search',SearchView.as_view(),name = 'search'),
    path('follow-unfollow-user',follow_unfollow_user,name = 'follow-unfollow'),
    path('login-user',store_login_info,name = 'login-user'),
    path('logout/<slug>',logout_information,name = 'logout'),
    path('send-friend-request',send_friend_request_or_remove,name = 'friend-request'),
    path('mark-as-read-delete',mark_as_read_delete,name = 'mark-as-read-delete'),
    path('accept-friend-request',accept_friend_request,name = 'accept-friend-request'),

]

# creating image url
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)