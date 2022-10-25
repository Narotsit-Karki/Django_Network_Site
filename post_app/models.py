from django.db import models
from home.models import *
from django.db.models import Q
# Create your models here.
from home.models import UserProfile

REACTIONS = (
    ('like','Like'),
    ('love', 'Love'),
    ('haha', 'Haha'),
    ('sad', 'Sad'),
    ('wow', 'Wow'),
    ('angry', 'Angry'),
    ('none','None'),
)

class PostReaction(models.Model):
    post_slug = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile,related_name='reacted_user',on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=500,choices= REACTIONS)
    def __str__(self):
        return f' {self.user} : {self.post_slug} : {self.reaction_type}'

class PostComment(models.Model):
    post_slug = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile,related_name='comment_user',on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} : {self.pos_slug}"



class UserPost(models.Model):

    slug = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    description = models.TextField()
    post_image = models.ImageField(upload_to=f'post_image',null = True, blank = True)
    post_video = models.FileField(upload_to='post_video', null = True,blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    snap_message = models.CharField(blank=True,null=True,max_length=800)

    def Post_Reactions(self):
        reactions = PostReaction.objects.filter(post_slug = self.slug)
        return reactions

    def Post_Comments(self):
        comments = PostComment.objects.filter(post_slug = self.slug)
        return comments

    def reacted_users_list(self):
        reactions = self.Post_Reactions()
        return [reaction.user for reaction in reactions]

    def comments_user_list(self):
        comments = self.Post_Comments()
        return [ comment.user for comment in comments]

    def __str__(self):
        return f"< {self.user.username} : {self.slug} : {self.created_at}"

class SavedPost(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost,on_delete=models.CASCADE)
    is_saved = models.BooleanField(default = True)
    def __str__(self):
        return f' < {self.user} : {self.post}'

class HiddenPost(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default = True)
    def __str__(self):
        return f' < {self.user} : {self.post}'


