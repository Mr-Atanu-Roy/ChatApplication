from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User, UserContacts
from chat.models import Group


# Create your views here.

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








