from django.contrib import admin
from .models import *

# Register your models here.
class UserPostAdmin(admin.ModelAdmin):
    list_filter = ('slug','user','created_at')
    list_display = ('slug','user','created_at','description')

class PostReactionAdmin(admin.ModelAdmin):
    list_filter = ('post_slug', 'user')
    list_display = ('post_slug','user','reaction_type')

class PostCommentAdmin(admin.ModelAdmin):
    list_filter = ('post_slug', 'user')
    list_display = ('post_slug','user','comment')

admin.site.register(UserPost,UserPostAdmin)
admin.site.register(PostReaction,PostReactionAdmin)
admin.site.register(PostComment,PostCommentAdmin)