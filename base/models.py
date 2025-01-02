from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Many to One Relationship

class Topic(models.Model):
    name = models.CharField(max_length=200)
  
    def __str__(self) -> str:
        return self.name
    

class Room(models.Model):
    host = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null=True (can be blank)
    participants = models.ManyToManyField(User, related_name='joined_rooom')
    updated = models.DateTimeField(auto_now=True)  # date time changes everytime we save. 
    created = models.DateTimeField(auto_now_add=True)  # created date shown
    # models have default id created starting from 1.
    

    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self) -> str:
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{str(self.user), self.room, self.body}"


# class UserProfile(models.Model):
    # 

class TopicFollowing(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return f"{str(self.user)}, {self.topic}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    about = models.TextField(null=True, max_length=300)
    profile_pic = models.ImageField(upload_to="images/", null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self) -> str:
        return f"{str(self.user)}, {str(self.about)}"
    

class FollowUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='following_set')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{str(self.user)}, {str(self.following)}"    