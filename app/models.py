from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    grp_name = models.CharField(max_length=255)

    def __str__(self):
        return self.grp_name

class chat_message(models.Model):
    message = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.username}:{self.message}' 
    
class Friend(models.Model):
    user = models.CharField(max_length=200)
    friend = models.CharField(max_length=200)

    def __str__(self):
        return self.friend

class friend_request(models.Model):
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)

    