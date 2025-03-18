from django.urls import path
from .consumers import *

ws_patterns=[
    path('ws/<str:room_name>/', ChatConsumer.as_asgi()),
]