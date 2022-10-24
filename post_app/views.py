from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from django.contrib import messages
import json

from notifications.signals import notify

from home.views import BaseView
from home.models import UserProfile
from .models import *
import os
from home.views import notification_messsage
from django.shortcuts import get_object_or_404, redirect, render

from django.db.models import Q
# Create your views here.



@login_required
def like_unlike_post(request):

    if request.method == "POST":
        post = get_object_or_404(UserPost, slug=request.POST.get('post_slug'))
        reaction = request.POST.get('reaction')

        if PostReaction.objects.filter(user = request.user , post_slug = post.slug).exists():
            reaction_obj = PostReaction.objects.get(user = request.user , post_slug = post.slug)
            # if user clicked previous reaction unreact
            if reaction_obj.reaction_type == reaction:
                reaction_obj.reaction_type = 'none'
                post.users_reacted.remove(request.user)
                reacted = False

            else:
                # if user clicked other reaction add them to user_reacted list
                if request.user not in post.users_reacted.get_queryset():
                    post.users_reacted.add(request.user)

                reaction_obj.reaction_type = reaction
                reacted = True


            reaction_obj.save()
        else:
            PostReaction.objects.create(user = request.user , post_slug = post.slug, reaction_type = reaction)

            post.users_reacted.add(request.user)
            new_reaction = PostReaction.objects.filter(user=request.user, post_slug=post.slug, reaction_type=reaction)
            post.reaction.add(new_reaction)
            reacted = True

        post.save()

        total_reactions = post.users_reacted.count()
        ctx = {'total_reactions': total_reactions,'reacted': reacted}

        #send notification to the user for reacted and not to the same user

        if reacted and post.user != request.user:
            notify.send(sender = request.user , recipient = post.user, verb = 'bxs-like', description = f'reacted to your post {post.description[:30]}...')

        return HttpResponse(json.dumps(ctx), content_type='application/json')

    ctx = {'data':'None'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')



@login_required
def create_a_new_post(request):
    if request.method == "POST":
        description = request.POST['description']
        image_file = request.FILES.get('photo_upload')
        video_file = request.FILES.get('video_upload')

        new_post = UserPost.objects.create(
            user=request.user,
            slug=os.urandom(6).hex(),
            description=description,
            post_image=image_file,
            post_video=video_file,
        )
        new_post.save()

        if request.user.user_followers.count() > 0:
            notify.send(sender=request.user,
                        recipient=request.user.user_followers.all(),
                        verb='Post Message',
                        description=notification_messsage['new-post'],
                        icon='images'
                        )

    return redirect(request.META['HTTP_REFERER'])


@login_required
def save_unsave_post(request, slug):
    post = get_object_or_404(UserPost, slug=slug)
    save_post_obj, saved = SavedPost.objects.get_or_create(user=request.user, post=post, is_saved=True)
    if saved:
        messages.success(request, f'Post Saved from {{post.user.username}}')
    else:
        save_post_obj.is_saved = False
        save_post_obj.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def hide_unhide_post(request, slug):
    post = get_object_or_404(UserPost, slug=slug)
    save_post_obj, created = HiddenPost.objects.get_or_create(user=request.user, post=post, is_hidden=True)
    # if the post was hidden unhide it
    if not created:
        save_post_obj.is_hidden = False
        save_post_obj.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_post(request, slug):
    try:
        post = get_object_or_404(UserPost, user=request.user, slug=slug)
        post.delete()
    except ObjectDoesNotExist:
        pass
    return redirect(request.META['HTTP_REFERER'])



class EditPost(BaseView):
    def post(self, request, slug):
        if request.method == "POST":
            description = request.POST['description']
            image_file = request.FILES.get('photo_upload')
            video_file = request.FILES.get('video_upload')
            post = get_object_or_404(UserPost, user=request.user, slug=slug)

            if post.post_image:
                if os.path.exists(post.post_image.path):
                    os.remove(post.post_image.path)
            else:
                if os.path.exists(post.post_video.path):
                    os.remove(post.post_video.path)



        return redirect(request.META['HTTP_REFERER'])

    def get(self, request, slug):
        post = get_object_or_404(UserPost, user=request.user, slug=slug)
        self.view['Edit_Post'] = post
        self.view['User_Profile'] = request.user

        return render(request, 'edit-post.html', self.view)
