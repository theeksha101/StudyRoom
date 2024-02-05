from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, UserFollowing

class TopicFollowing(admin.ModelAdmin):
    list_display = ['user', 'topic']


admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(UserFollowing, TopicFollowing)
