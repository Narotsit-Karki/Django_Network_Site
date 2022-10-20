from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.cache import cache
from social_media import settings
# Create your models here.
GENDER = (
    ('male' ,'Male'),
    ('female','Female'),
    ('others','Others'),
    ('','rather not say')
)
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=800, unique=True)
    fname = models.CharField(max_length = 500)
    lname = models.CharField(max_length=500)
    email = models.EmailField(max_length = 600, unique=True)
    country = models.CharField(max_length=400)
    city = models.CharField(max_length = 500)
    dob = models.DateField()
    description = models.TextField(blank=True)
    gender = models.CharField(choices=GENDER,max_length=100)
    job = models.TextField(blank = True)
    profile_pic = models.ImageField(upload_to = 'media/profile_pic', default = 'default.png')
    following = models.ManyToManyField('self',symmetrical=False, blank = True)

    def __str__(self):
        return f"{self.username}"

    def last_seen(self):
        return cache.get(f'seen_{self.user.username}')

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False






