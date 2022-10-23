
from django.urls import path ,include
from .views import *

urlpatterns = [
    path('create-new-post',create_a_new_post, name = 'create-new-post'),
    path('save-post/<slug>',save_post,name = 'save-post'),
    path('hide-post/<slug>',hide_post,name = 'hide-post'),
    path('delete-post/<slug>',delete_post,name = 'delete-post'),
    path('edit-post/<slug>',EditPost.as_view(),name = 'edit-post')
]

