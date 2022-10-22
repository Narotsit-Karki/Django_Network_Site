
from django.urls import path ,include
from .views import *

urlpatterns = [
    path('create-new-post',create_a_new_post, name = 'create-new-post'),
]

