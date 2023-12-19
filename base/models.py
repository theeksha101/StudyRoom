from django.db import models

# Create your models here.
class Room(models.Model):
    # host = 
    # topic = 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # null=True (can be blank)
    # participants = models.
    updated = models.DateTimeField(auto_now=True)  # date time changes everytime we save. 
    created = models.DateTimeField(auto_now_add=True)  # created date shown

    def __str__(self) -> str:
        return self.name