from django.urls import path
from .views import *

urlpatterns = [
    
    path('ak/home/',home,name='home-page'),                              # home.html
    path('ak/home/chats/',user_chat_group,name='user_group'),            # display the groups of user and his friends. [chat_user.html]
    path('ak/home/add_friends/',all_users,name='add-friend'),            # display all the user available on platform. [all_user.html]
    path('ak/home/add_friend/<str:user1>/<str:user2>/',add_friend),      # add's a friend request in database.
    path('ak/home/friend_request/',show_request,name='friend-request'),  # Show's friend request available for user. [fiend_request.html]
    path("ak/home/accept_reject/<str:sender>/<str:status>/",accept_reject,name="accept_reject"),   # accepts or reject friend request. [friend_request.html]
    path('ak/home/chat/<str:user1>/<str:user2>/',show_chat),             # show the chatting interface and chats for one to one chat.[base.html]
    path('ak/home/chat/<str:Grp_name>/',show_group_chat),                # show the chatting interface and chats for group chat.[base.html]
   
]   