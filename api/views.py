from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from accounts.models import User, UserContacts
from chat.models import Group

from accounts.utils import check_str_special, cache_set, cache_get
from chat.model_func import get_user_chats


# Create your views here.

@login_required(login_url="/auth/login")
@csrf_exempt
def search_contact(request):
    '''
    Handel the dynamic searching of contacts on contact page
    '''

    response = {}
    status = 0,
    data = None,
    error = "no data"

    try:
        if request.method == "POST":
            phone = request.POST.get("phone").strip()

            #validate phone
            if phone != request.user.phone:
                if phone.isdigit() and len(phone) == 10:

                    key = f"{phone}_searched"
                    #get the cached data
                    cached_data = cache_get(key)

                    #check if data is cached
                    if cached_data:
                        return JsonResponse(cached_data, safe=False)
                    else:
                        #search for user
                        user = User.objects.filter(phone=phone).first()
                        
                        #check if user exists
                        if user is None:
                            status = 404
                            error = "this phone number does not have whatsapp account"
                        else:
                            profile_pic = None
                            if user.profile_pic != "":
                                profile_pic = f"/media/{user.profile_pic}"
                            
                            data = {
                                "name": user.first_name+" "+user.last_name,
                                "phone": user.phone,
                                "profile_pic": profile_pic
                            }
                            status = 200
                            error = None
                            
                        #set the cache
                        cache_set(key, {
                            "status": status,
                            "data": data,
                            "error": error
                        })

                else:
                    status = 400
                    error = "invalid phone number"
            else:
                status = 400
                error = "can not add your phone number"

        else:
            status = 405
            error = "only POST method is allowed"


    except Exception as e:
        print(e)
        pass

    response["status"] = status
    response["data"] = data
    response["error"] = error

    return JsonResponse(response, safe=False)



@login_required(login_url="/auth/login")
@csrf_exempt
def add_to_contact(request):
    '''
    Handel the addition of contact to user account
    '''


    response = {}
    status = 0,
    message = None,
    error = "no data"

    try:
        if request.method == "POST":
            phone = request.POST.get("phone").strip()
            print(phone)
            #validate phone
            if phone != request.user.phone:
                if phone.isdigit() and len(phone) == 10:
                    #search for user
                    user = User.objects.filter(phone=phone).first()
                    
                    #check if user exists
                    if user is None:
                        status = 404
                        error = "this phone number does not have whatsapp account"
                    else:
                        #getting current user contacts instance
                        get_user_contacts = UserContacts.objects.filter(user=request.user).first()

                        if get_user_contacts:
                            #check if user is already in user's contact
                            if not user in get_user_contacts.contacts.all():
                                get_user_contacts.contacts.add(user)
                                get_user_contacts.save()

                                message = f"{phone} added to contact"
                                status = 201
                                error = None
                            else:
                                error = f"{phone} is already in your contact"
                                status = 400
                else:
                    status = 400
                    error = "invalid phone number"
            else:
                status = 400
                error = "can not add your phone number"

        else:
            status = 405
            error = "only POST method is allowed"


    except Exception as e:
        print(e)
        pass

    response["status"] = status
    response["message"] = message
    response["error"] = error

    return JsonResponse(response, safe=False)


@login_required(login_url="/auth/login")
def search_chats(request):
    '''
    Handel dynamic chat searching on chat nav bar
    '''

    response = {}
    status = 0,
    data = None,
    error = "no data"

    try:
        if request.method == "GET":
            #get the search query
            query = request.GET.get("query")
            
            #check if query is valid char
            if not check_str_special(query):

                key = f"{request.user}_chat_searched_{query}"
                #get the cached data
                cached_data = cache_get(key)

                #check if cache exists
                if cached_data:
                    return JsonResponse(cached_data, safe=False)
                else:
                    chats = get_user_chats(request.user, query)

                    #check if any chat is found
                    if chats is not None:
                        data = []

                        #iterate over each item and add to data as dict
                        for chat in chats:
                            data.append({
                                "url": f"/chat/{chat.type}/{chat.id}",
                                "name": chat.name,
                                "desc": chat.description,
                                "chat_pic": f"/media/{chat.group_pic}",
                            })

                        status = 200
                        error = None
                    else:
                        status = 204
                        error = "nothing found"

                    #set the cache
                    cache_set(key, {
                        "status": status,
                        "data": data,
                        "error": error
                    })

            else:
                status = 400
                error = "invalid group name"
        else:
            status = 405
            error = "only GET method is allowed"

    except Exception as e:
        print(e)
        pass

    response["status"] = status
    response["data"] = data
    response["error"] = error

    return JsonResponse(response, safe=False)


@login_required(login_url="/auth/login")
def exit_group(request):
    '''
    handel group exit of current user
    '''
    
    response = {}
    status = 0,
    message = "",
    error = "no data"

    try:
        if request.method == "GET":
            #get the group_id
            group_id = request.GET.get("group_id")

            group = Group.objects.filter(id=group_id).first()
            #check if group exists
            if group is not None:
                #check if user is part of the group
                if request.user in group.members.all():
                    try:
                        #check if user is owner
                        if group.owner == request.user:
                            #make some one else the owner
                            group.owner = group.members.exclude(id=request.user.id).first()
                            group.save()

                        #remove the user from group
                        group.members.remove(request.user)

                        
                        status = 201
                        error = None
                        message = "user removed"
                    except Exception as e:
                        print(e)
                        status = 500
                        error = "something went wrong"
                else:
                    status = 401
                    error = "invalid user"

            else:
                status = 400
                error = "invalid group name"
        else:
            status = 405
            error = "only GET method is allowed"

    except Exception as e:
        print(e)
        pass

    response["status"] = status
    response["message"] = message
    response["error"] = error

    return JsonResponse(response, safe=False)



@login_required(login_url="/auth/login")
def delete_group(request):
    '''
    handel deletion of group if user is owner
    '''
    
    response = {}
    status = 0,
    message = "",
    error = "no data"

    try:
        if request.method == "GET":
            #get the group_id
            group_id = request.GET.get("group_id")

            group = Group.objects.filter(id=group_id).first()
            #check if group exists
            if group is not None:
                #check if user is group owner
                if group.owner == request.user:
                    try:
                        #delete the group
                        group.delete()
                        
                        status = 201
                        error = None
                        message = "group deleted"
                    except Exception as e:
                        status = 500
                        error = "something went wrong"
                else:
                    status = 401
                    error = "you are not group owner"

            else:
                status = 400
                error = "invalid group name"
        else:
            status = 405
            error = "only GET method is allowed"

    except Exception as e:
        print(e)
        pass

    response["status"] = status
    response["message"] = message
    response["error"] = error

    return JsonResponse(response, safe=False)


