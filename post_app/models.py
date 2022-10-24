from django.db import models
from home.models import *
from django.db.models import Q
# Create your models here.


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



class UserPost(models.Model):

    slug = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    description = models.TextField()
    post_image = models.ImageField(upload_to=f'post_image',null = True, blank = True)
    post_video = models.FileField(upload_to='post_video', null = True,blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    snap_message = models.CharField(blank=True,null=True,max_length=800)

    users_reacted = models.ManyToManyField(UserProfile,related_name= 'users_reacted_list')



    def __str__(self):
        return f"< {self.user.username} : {self.slug} : {self.created_at}"



    def __str__(self):
        return f"< {self.user} : {self.post_slug} : {self.reaction_type}"

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


