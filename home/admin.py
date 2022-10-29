from django.contrib import admin
from django.utils.html import format_html

from .models import *


# Register your models here.

class ProfileUser(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(
            f'''<img src = '{obj.profile_pic.url}' 
                    class = 'avatar' 
                    style= 'object-fit: cover;
                    vertical-align: middle;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;'
                />
                ''' )

    image_tag.short_description = 'Profile Pic'
    list_display = ('image_tag', 'username', 'email','is_staff','country')

admin.site.register(UserProfile, ProfileUser)

class LoginSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_date', 'device', 'device_type', 'browser' )

admin.site.register(LoginSessionInfo,LoginSessionAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user')

admin.site.register(FriendRequest,FriendRequestAdmin)