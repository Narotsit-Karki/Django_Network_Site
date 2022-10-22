from django.db import models
from home.models import *

# Create your models here.

class UserPost(models.Model):

    slug = models.CharField(max_length=500)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    description = models.TextField()
    post_image = models.ImageField(upload_to=f'post_image',null = True, blank = True)
    post_video = models.FileField(upload_to='post_video', null = True,blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    post_likes= models.IntegerField(default=0)
    post_comments = models.IntegerField(default=0)

    def __str__(self):
        return f"< {self.user.username} : {self.slug} : {self.created_at}"