from django.contrib import admin

# Register your models here.
from .models import Room, Topic, Message, TopicFollowing, UserProfile

class TopicFollowingManager(admin.ModelAdmin):
    list_display = ['user', 'topic']


class MessageManager(admin.ModelAdmin):
    list_display = ['user', 'room', 'body']


admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message, MessageManager)
admin.site.register(TopicFollowing, TopicFollowingManager)
admin.site.register(UserProfile)