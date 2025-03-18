from app.models import Group
from django.db import models
from django.contrib.auth.models import User

class group_chat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin=models.BooleanField()
    member=models.ForeignKey(User,on_delete=models.CASCADE)
    gp_discription=models.CharField(max_length=999)
