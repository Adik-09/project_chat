from django.urls import path
from .views import *

urlpatterns = [
    path('ak/home/create_group/',create_group,name='create_group'),
    path('ak/home/create_group/<str:grp_name>/',show_members, name='show_members'),
    path('ak/home/create_group/add_mem/<str:grp_name>/<str:member>/',add_member),
    path('ak/home/create_group/delete_mem/<str:grp_name>/<str:member>/',delete_member),
    path('ak/home/group_details/<str:grp_name>/',group_details),
    path('ak/home/delete_group/<str:grp_name>/',delete_group)
]
