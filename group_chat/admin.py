from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(group_chat)
class group_chat_admin(admin.ModelAdmin):
    list_display=['member','admin','group']