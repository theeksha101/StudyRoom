from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .models import Room, Topic, UserFollowing, Message
from .forms import RoomForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


class RoomService:        

    def __init__(self):
        pass

    # Entity Layer
    def get_room(self, pk):
        
        return Room.objects.get(id=pk)
    
    def get_room_msg(self, pk):
        return Message.objects.filter(room=pk)
    
    def get_form(self, pk):
        return RoomForm(instance=self.get_room(pk=pk))
    
    # DAO Layer
    def create_message(self, user, incoming_msg, pk):
        msg = Message.objects.create(user=user, room=self.get_room(pk), body=incoming_msg)
        msg.save()
            
    def create_room(self, room_info):
        """
        room_info includes [name, host, topic, description]
        """
        form = RoomForm(room_info)
        if form.is_valid():
            form.save()
        
    def update_room(self, room_info, pk):
        form = RoomForm(room_info, instance=self.get_room(pk=pk))
        if form.is_valid():
            form.save()

    def delete_room(self, pk):
        room = self.get_room(pk)
        room.delete()

    def _find_default_room(self):
        """
        Finds default room
        """
        return None
    

class UserService:

    def __init__(self):
        pass

    # Entity Layer
    def get_username(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception("User does not exist")

    
    # DAO Layer
    # ....

    # Service Layer
    def authenticate_user(self, username, password):
        pass
    
    def create_user(self, username, password, email, first_name, last_name):
        user = User.objects.create_user(username=username,
                password=password, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
    

    def user_topic(self, user, topic): 
        return UserFollowing.objects.get(user=user, topic=topic)
    
    
    def unfollow_topic(self, user, topic):
        topic_name = Topic.objects.get(name=topic)
        follow_entry = UserFollowing.objects.get(user=user, topic=topic_name)
        follow_entry.delete()

    def follow_topic(self, user, topic):
        topic_name = Topic.objects.get(name=topic)
        UserFollowing.objects.create(user=user, topic=topic_name)