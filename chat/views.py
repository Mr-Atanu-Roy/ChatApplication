from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from accounts.models import User
from chat.models import Group, ChatMessages

from accounts.utils import check_str_special
from accounts.model_func import get_user_contacts

from chat.model_func import get_group_messages

# Create your views here.

@login_required(login_url="/auth/login")
def chat_home(request):
    '''
    Handel home of application
    '''

    return render(request, 'chat/home.html')

    

@login_required(login_url="/auth/login")
def new_chat_group(request):
    '''
    Handel creation of new group chat group
    '''
    
    context = {}
    contacts = None
    selected_contacts = []
    group_name = group_desc = ""
    try:
        #get user contacts
        contacts = get_user_contacts(request.user)

        # handling POST request: Creation og group
        if request.method == "POST":
            #get the form data
            group_name = request.POST.get("group_name").strip()
            group_desc = request.POST.get("group_desc").strip()
            selected_contacts = request.POST.getlist("phone_checkbox")
            is_desc = False

            #validate group desc if its present
            if group_desc != "":
                if len(group_desc) > 6:
                    if len(group_desc) < 255:
                        if check_str_special(group_desc):
                            messages.error(request, "invalid group description")
                        else:
                            is_desc = True
                    else:
                        messages.error(request, "group description too long")
                else:
                    messages.error(request, "group description too short")
            else:
                is_desc = True

            #validate group name
            if len(group_name) < 15:
                if group_name != "" and not check_str_special(group_name) and len(group_name) > 1:

                    if is_desc:
                        #check if at least 2 contacts are selected
                        if len(selected_contacts) < 2:
                            messages.error(request, "Your group must have at least 2 contacts")
                        else:
                            group_members = [request.user]
                            for contact in selected_contacts:
                                #check if contacts are valid
                                if contact.isdigit() and len(contact) == 10:
                                    #get user from phone
                                    get_user = User.objects.filter(phone=contact).first()
                                    #check if user exists
                                    if get_user:
                                        group_members.append(get_user)
                            if len(group_members) >= 3:
                                #create new group
                                new_group = Group(name=group_name, owner=request.user)
                                #add desc if present
                                if group_desc != "":
                                    new_group.description = group_desc

                                #add image if present
                                if request.FILES.get('group_pic') is not None:
                                    new_group.group_pic = request.FILES.get('group_pic')
                                new_group.save()

                                #adding members
                                for users in group_members:
                                    new_group.members.add(users)
                                new_group.save()
                                
                                url = f"/chat/group/{new_group.id}"
                                
                                return redirect(url)
                else:
                    messages.error(request, "invalid group name")
            else:
                messages.error(request, "group name too long")

    except Exception as e:
        print(e)
        pass
    
    context["contacts"] = contacts
    context["group_name"] = group_name
    context["group_desc"] = group_desc
    context["selected_contacts"] = selected_contacts
    return render(request, 'chat/create_chat_group.html', context)
    




@login_required(login_url="/auth/login")
def chat_group(request, id):
    '''
    This view handel the chat page of group chats.
    '''
    context = {}
    group = group_msg = None
    try:
        
        #get the group instance from id
        group = Group.objects.filter(id=id).first()

        #check if group exists and user is a part of it
        if not group or request.user not in group.members.all():
            return HttpResponse("<h3>INVALID GROUP</h3>")
        
        #get group messages
        group_msg = get_group_messages(group)

        
    except Exception as e:
        print(e)
        pass
    
    context["group_msg"] = group_msg
    context["group"] = group
    return render(request, 'chat/chat_group.html', context)



