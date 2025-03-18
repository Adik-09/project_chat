from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from group_chat.models import *
from django.db.models import Count

@login_required  # display chats between two people.
def show_chat(request,user1,user2): 
    
    Grp_name=f"{min(user1,user2)}_{max(user1,user2)}"
    grp = Group.objects.filter(grp_name=Grp_name).first()
    chats = []

    if grp:
        chats = chat_message.objects.filter(group=grp).order_by('timestamp')  # Order messages by time
    else:
        grp = Group.objects.create(grp_name=Grp_name)
        grp.save()
    return render(request,'main_chat.html',{'chats':chats,'grpname':Grp_name,'group':'single'})


@login_required  # display chats between a group.
def show_group_chat(request,Grp_name): 
    
    grp = Group.objects.filter(grp_name=Grp_name).first()
    chats = chat_message.objects.filter(group=grp).order_by('timestamp')  # Order messages by time     
    print(chats)  
    return render(request,'main_chat.html',{'chats':chats,'grpname':Grp_name,'group':'group'})


@login_required  # render's home page.
def home(request):
   return render(request,'home.html')


@login_required #  display the user available on app.
def all_users(request): 
    searched_user=None
    if request.method=="POST":
        user_search=request.POST.get('userSearch')
        if user_search != "":   
            searched_user=User.objects.filter(username=user_search).first()
            if searched_user == None:
                messages.error(request,"User not found")  
    
    users=User.objects.order_by('?')[:6]
    return render(request,'all_user.html',{'users':users,'searched_user':searched_user})


@login_required  # send friend request in database.   
def add_friend(request, user1, user2):

    # check the  user is already friend or not.
    if Friend.objects.filter(user=user1,friend=user2).exists():
        messages.error(request,"The user is already your friend.")
    else:
        # Check if a friend request already exists
        if friend_request.objects.filter(sender=user1, receiver=user2).exists():
            messages.success(request, "Request already sent.")
        else:
            try:
                friend_request.objects.create(sender=user1, receiver=user2)
                messages.success(request, "Friend request sent successfully.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                
    return redirect('add-friend')


@login_required  # diaplay the request available for user. 
def show_request(request):
    fr_req=friend_request.objects.filter(receiver=str(request.user))
    return render(request,'friend_request.html',{'fr_req':fr_req})


@login_required  # display the friends of user and the groups.
def user_chat_group(request):
    # Get friends of the logged-in user
    friends = Friend.objects.filter(user=request.user)

    # Get groups the user is a member of and annotate with member count
    user_groups = (
        group_chat.objects.filter(member=request.user)
        .select_related("group")
        .annotate(member_count=Count("group__group_chat"))
    )

    return render(
        request,
        "chat_user.html",
        {"friends": friends, "groups": user_groups},
    )


@login_required # logic to accept and reject friend request, after which it adds sender in friend list.
def accept_reject(request, sender, status):
    if request.method == "POST":
    
        fr_req = get_object_or_404(friend_request, sender=sender, receiver=str(request.user))

        if status == "accept":
            # similar to fr=Friend(user=str(request.user),friend=sender) but adds multiple data.
            Friend.objects.bulk_create([
                Friend(user=sender, friend=str(request.user)),
                Friend(user=str(request.user), friend=sender),
            ])
            messages.success(request, "Request accepted successfully")
        elif status == "reject":
            messages.error(request, "Request rejected successfully")
    
        fr_req.delete()
        
    return redirect('friend-request')

