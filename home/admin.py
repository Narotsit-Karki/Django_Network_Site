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
    list_display = ('user', 'image_tag', 'dob', 'city', 'gender')

admin.site.register(Profile, ProfileUser)
