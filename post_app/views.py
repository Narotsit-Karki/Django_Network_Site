
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect , render


from .models import UserPost
import os
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

    return redirect(request.META['HTTP_REFERER'])
