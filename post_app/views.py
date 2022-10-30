from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
import json
from notifications.signals import notify
from home.views import BaseView , ProfileView
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
        reaction_obj , created = PostReaction.objects.get_or_create(post_slug = post.slug , user = request.user,reaction_type = reaction)

        if created:
            reacted = True
            if PostReaction.objects.filter(~Q(reaction_type = reaction),post_slug = post.slug ,user = request.user, ).exists():
                reaction_obj = PostReaction.objects.get(~Q(reaction_type=reaction), post_slug=post.slug, user=request.user)
                reaction_obj.delete()
            if request.user != post.user:
                notify.send(sender = request.user , recipient = post.user,verb = 'bxs-like', description = f'reacted to your post {post.description[:30]}...')

        else:
            reaction_obj.delete()
            reacted = False

        total_reactions = post.Post_Reactions().count()
        ctx = {'total_reactions': total_reactions,'reacted': reacted}
        #send notification to the user for reacted and not to the same user
        return HttpResponse(json.dumps(ctx), content_type='application/json')

    ctx = {'data':'None'}
    return HttpResponse(json.dumps(ctx), content_type='application/json')



def post_validity(description  ,image_file , video_file):
    description = description.split()
    if image_file is None and video_file is None and len(description) == 0:
        return False
    else:
        return True

@login_required
def create_a_new_post(request):
    if request.method == "POST":
        description = request.POST['description']
        image_file = request.FILES.get('photo_upload')
        video_file = request.FILES.get('video_upload')
        if post_validity(description,image_file,video_file):
            new_post = UserPost.objects.create(
                            user=request.user,
                            slug=os.urandom(6).hex(),
                            description=description,
                            post_image=image_file,
                            post_video=video_file,
                        )
            new_post.save()
            # sending notifications to all followers if user has follower count > 0
            if request.user.user_followers.count() > 0:
                notify.send(sender=request.user,
                        recipient=request.user.user_followers.all(),
                        verb='bxs-images',
                        description=notification_messsage['new-post'],
                        )

    return redirect(request.META['HTTP_REFERER'])



@login_required
def save_unsave_post(request, slug):
    if request.method == "GET":
        post = get_object_or_404(UserPost, slug=slug)
        save_post_obj, saved = SavedPost.objects.get_or_create(user=request.user, post=post, is_saved=True)
        if saved:
            messages.success(request, f'Post Saved from {{post.user.username}}')
        else: #if post was saved previously now we unsave it
            save_post_obj.is_saved = False
            save_post_obj.save()

    return redirect(request.META['HTTP_REFERER'])



@login_required
def hide_unhide_post(request, slug):
    if request.method == "GET":
        post = get_object_or_404(UserPost, slug=slug)
        save_post_obj, created = HiddenPost.objects.get_or_create(user=request.user, post=post, is_hidden=True)
        # if the post was hidden unhide it
        if not created:
            save_post_obj.is_hidden = False
            save_post_obj.save()

    return redirect(request.META['HTTP_REFERER'])



@login_required
def delete_post(request, slug):
    if request.method == "GET":
        post = get_object_or_404(UserPost, user=request.user, slug=slug)
        post.delete()

    return redirect(request.META['HTTP_REFERER'])





class EditPost(ProfileView):
    def post(self, request, slug):
        if request.method == "POST":
            description = request.POST['description']
            image_file = request.FILES.get('photo_upload')
            video_file = request.FILES.get('video_upload')
            post_obj = get_object_or_404(UserPost, user=request.user, slug=slug)

            if post_validity(description,image_file,video_file):
                #update post image by removing the old image and adding new one
                if post_obj.post_image and image_file is not None:
                    if os.path.exists(post_obj.post_image.path):
                        os.remove(post_obj.post_image.path)
                    post_obj.post_image = image_file
                else:# update post video by removing the old video and adding new one
                    if post_obj.post_video and video_file is not None:
                        if os.path.exists(post_obj.post_video.path):
                            os.remove(post_obj.post_video.path)
                            post_obj.post_video = video_file

                if description is not None: #update description
                    post_obj.description = description

                post_obj.save()

        return redirect(f"/profile/{request.user.username}")

    def get(self, request, slug):
        self.view
        post = get_object_or_404(UserPost, user=request.user, slug=slug)
        self.view['Edit_Post'] = post
        return render(request, 'edit-post.html', self.view)


# validates space and blanks in comment
def validate_comment(comment):
    comment = comment.split()
    if len(comment) != 0:
        return True
    else:
        return False



@login_required
def post_comment(request,slug):
    if request.method == 'POST':
        post = get_object_or_404(UserPost,slug = slug)
        comment = request.POST.get('comment')
        if validate_comment(comment):
            new_comment = PostComment.objects.create(
            post_slug = slug,
            user = request.user,
            comment = comment
            )
            new_comment.save()

            # send notification
            if request.user != post.user:
                notify.send(sender = request.user , recipient = post.user, verb = 'bxs-quoute-right' , description = f'commented on your post {post.description[:30]}')

    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_comment(request,slug,id):
    if request.method == 'GET':
        post_comment = get_object_or_404(PostComment,post_slug=slug,id = id)
        post_comment.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def edit_comment(request,slug,id):
    if request.method == 'POST':
        post_comment = get_object_or_404(PostComment,post_slug = slug, id = id)
        new_comment = request.POST.get('edit-comment')
        if validate_comment(new_comment) and post_comment.comment != new_comment:
            post_comment.comment = new_comment
            post_comment.save()

    return redirect(request.META['HTTP_REFERER'])

@login_required
def add_photos(request,username):
    if request.method == 'POST' and request.user.username == username:
        photos = request.FILES.getlist('upload_photos')
        for p in photos:
            photo_obj = UserImage.objects.create(
                slug = os.urandom(6).hex(),
                user = request.user,
                image = p
                )
            photo_obj.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_photos(request,username):

    if request.method == "POST" and request.user.username == username:
        delete_photos_list_slug = []
        for photo in UserImage.objects.filter(user = request.user):
                delete_photos_list_slug.append(request.POST.get(photo.slug))

        for slug in delete_photos_list_slug:
            if slug is not None:
                try:
                    del_photo = UserImage.objects.get(user = request.user,slug = slug)
                    del_photo.delete()
                except Exception:
                    pass

        return redirect(request.META['HTTP_REFERER'])