from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Group)

@admin.register(chat_message)
class chat_mes_admin(admin.ModelAdmin):
    list_display=['author','message','group']

@admin.register(Friend)
class friend_admin(admin.ModelAdmin):
    list_display=['user','friend']
    
admin.site.register(friend_request)

