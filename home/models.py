from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import datetime
from django.core.cache import cache
from social_media import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
GENDER = (
    ('male' ,'Male'),
    ('female','Female'),
    ('others','Others'),
    ('','rather not say')
)


class UserProfile(AbstractUser):
    # username = models.CharField(max_length=400, unique= True)
    country = models.CharField(max_length=400)
    city = models.CharField(max_length = 500)
    dob = models.DateField(blank = True , null = True)
    phone = models.IntegerField(blank=True, null = True)
    description = models.TextField(blank=True, null = True)
    gender = models.CharField(choices=GENDER,max_length=100, null = True)
    job = models.TextField(blank = True, null = True)
    profile_pic = ResizedImageField(size = [ 512, 512],upload_to = 'profile_pic', default = 'default.png', null = True ,force_format = 'PNG')

    user_friends = models.ManyToManyField('self',blank = True , symmetrical=False, related_name='users_friends')
    user_followers = models.ManyToManyField('self',blank = True , symmetrical= False,  related_name='users_followers')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f"{self.username}"

    def Hidden_Post(self):
        hidden_posts = HiddenPost.objects.filter(user = self)

    def last_seen(self):
        return cache.get(f'seen_{self.username}')

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



class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile,related_name='from_user',on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile,related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f" < {self.from_user} ---> {self.to_user} >"

class LoginSessionInfo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500)
    os = models.CharField(max_length=200,blank=True)
    device = models.CharField(max_length=200,blank = True)
    login_date = models.DateField(auto_now_add=True)
    login_time = models.TimeField(auto_now_add=True)
    device_type = models.CharField(max_length=200,blank=True)
    browser = models.CharField(max_length=300,blank=True)
    active = models.BooleanField()

    def __str__(self):
        return f"< {self.user}: {self.device} : {self.login_date} : {self.login_time}"


