from django.db import models
from django.contrib.auth.models import User
# Create your models here.
GENDER = (
    ('male' ,'Male'),
    ('female','Female'),
    ('others','Others'),
    ('','rather not say')
)
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=400)
    address = models.CharField(max_length = 500)
    dob = models.DateField()
    description = models.TextField(blank=True)
    gender = models.CharField(choices=GENDER,max_length=100)
    job = models.TextField(blank = True)
    profile_pic = models.ImageField(upload_to = 'media/profile_pic', default = 'media/profile_pic/default.png')






