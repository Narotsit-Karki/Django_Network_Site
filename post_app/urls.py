
from django.urls import path ,include
from .views import *

urlpatterns = [
    path('create-new-post',create_a_new_post, name = 'create-new-post'),
    path('save-unsave-post/<slug>',save_unsave_post,name = 'save-unsave-post'),
    path('hide-unhide-post/<slug>',hide_unhide_post,name = 'hide-unhide-post'),
    path('delete-post/<slug>',delete_post,name = 'delete-post'),
    path('edit-post/<slug>',EditPost.as_view(),name = 'edit-post'),
    path('like-unlike-post',like_unlike_post,name = 'like-unlike-post')
]

