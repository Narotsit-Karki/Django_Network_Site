
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect , render
from notifications.signals import notify
from django.contrib import messages

from home.views import BaseView

from home.models import UserProfile
from .models import *
import os

from home.views import notification_messsage


# Create your views here.


@login_required
def create_a_new_post(request):
    if request.method == "POST":
        description = request.POST['description']
        image_file = request.FILES.get('photo_upload')
        video_file = request.FILES.get('video_upload')

        new_post = UserPost.objects.create(
            user = request.user,
            slug = os.urandom(6).hex(),
            description = description,
            post_image = image_file,
            post_video = video_file,
            post_likes = 0,
            post_comments = 0,
        )
        new_post.save()

        if request.user.user_followers.count() > 0:
            notify.send(sender = request.user ,
                        recipient = request.user.user_followers.all(),
                        verb = 'Post Message',
                        description = notification_messsage['new-post'],
                        icon = 'images'
                        )

    return redirect(request.META['HTTP_REFERER'])


@login_required
def save_post(request , slug):

    try:
        post = UserPost.objects.get(slug = slug)
        save_post_obj , saved = SavedPost.objects.get_or_create(user = request.user , post = post)
        if saved:
            messages.success(request,f'Post Saved from {{post.user.username}}')
    except ObjectDoesNotExist:
        raise Http404

    return redirect(request.META['HTTP_REFERER'])



@login_required
def hide_post(request,slug):
    try:
        post = UserPost.objects.get(slug=slug)
        save_post_obj, saved = HiddenPost.objects.get_or_create(user=request.user, post=post)

    except ObjectDoesNotExist:
        raise Http404

    return redirect(request.META['HTTP_REFERER'])




@login_required
def delete_post(request , slug):
    try:
        post = UserPost.objects.get(user = request.user,slug = slug)
        post.delete()
    except ObjectDoesNotExist:
        pass
    return redirect(request.META['HTTP_REFERER'])




class EditPost(BaseView):
    def post(self,request, slug):
        if request.method == "POST":
            description = request.POST['description']
            image_file = request.FILES.get('photo_upload')
            video_file = request.FILES.get('video_upload')

        print("image file: ",image_file,"description: ", description,"video file: ",video_file)
        return redirect(request.META['HTTP_REFERER'])

    def get(self,request,slug):
        try:

           post = UserPost.objects.get(user = request.user , slug = slug)
           self.view['Edit_Post'] = post
           self.view['User_Profile'] = request.user

        except ObjectDoesNotExist:
            raise Http404
        return render(request,'edit-post.html',self.view)



