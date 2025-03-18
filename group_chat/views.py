from django.shortcuts import render,redirect,get_object_or_404
from app.models import Group,Friend
from .models import *
from django.contrib import messages

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        grp_discription=request.POST.get('gp_discription')
        grp=Group.objects.filter(grp_name=group_name).exists()
        
        if grp:
            messages.error(request,"Group already exits, Joined the group")
        else:
            gp=Group.objects.create(grp_name=group_name)
            gm=group_chat(group=gp,member=request.user,admin=True,gp_discription=grp_discription)
            gm.save()
            messages.success(request,'Group Created successfully')
            
        return redirect('user_group')
        
    return render(request,'create_group.html')


def show_members(request,grp_name):
    fr=Friend.objects.filter(user=str(request.user))
    gp=Group.objects.get(grp_name=grp_name)
    gp_member=group_chat.objects.filter(group=gp)
    return render(request,'add_user.html',{'grp_name':grp_name,'friend':fr,'gp_member':gp_member})


def add_member(request,grp_name,member):
    grp=Group.objects.get(grp_name=grp_name)
    mem=User.objects.get(username=member)
    gcp=group_chat.objects.filter(group=grp,member=mem).exists()

    if not gcp:
       gc=group_chat(group=grp,member=mem,admin=False)
       gc.save()
       messages.success(request,"Friend added in the group")
    else:
        messages.error(request,"User is already in the group")
    return redirect('show_members',grp_name)


def delete_member(request,grp_name,member):
    gp_name=Group.objects.get(grp_name=grp_name)
    gp_member=User.objects.get(username=member)
    gp_obj=group_chat.objects.filter(group=gp_name,member=gp_member)
    gp_obj.delete()
    messages.error(request,"Member removed successfully")
    return redirect('show_members',grp_name)

def group_details(request, grp_name):

    grp = Group.objects.get(grp_name=grp_name)
    group_details = group_chat.objects.filter(group=grp)
    gp_name=group_details[0].group
    grp_discription=group_details[0].gp_discription

    return render(request, 'group_detail.html', {'gp_details': group_details,'gp_name':gp_name,'grp_discription':grp_discription})


def delete_group(request,grp_name):
    grp =get_object_or_404(Group,grp_name=grp_name)
    adm=get_object_or_404(group_chat,group=grp,member=request.user)
    
    if adm.admin == True:
        adm.delete()
        grp.delete()
        messages.success(request,"Group deleted successfully.")
    else:
        messages.error(request,"Only admin can delete the group")
    
    return redirect('create_group')