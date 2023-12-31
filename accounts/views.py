from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import JsonResponse

from accounts.models import User
from accounts.utils import current_time, check_str_special, validate_email
from accounts.model_func import get_user_contacts

# Create your views here.


# user signup/registration view 
def signup(request):
    phone = first_name = password = ""
    context = {}
    try:

        #check if user is authenticated
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('home')
        else:
            try:
                if request.method == "POST":
                    phone = request.POST.get("phone")
                    first_name = request.POST.get("firstName")
                    password = request.POST.get("password")

                    #check if phone number is valid
                    if phone.isdigit() and len(phone)==10:

                        #check if first_name number is valid
                        if first_name != "" and not check_str_special(first_name):

                            #check if user with same phone number is registered
                            if User.objects.filter(phone = phone).first() is not None:
                                messages.error(request, "An account already exists with this phone number")
                            else:
                                #create user obj if everything is fine
                                new_user = User.objects.create_user(phone=phone, password=password)
                                new_user.first_name = first_name
                                new_user.save()

                                phone = first_name = password = ""

                                # login the user
                                auth.login(request, new_user)

                                #redirect user to profile page
                                return redirect('profile')

                        else:
                            messages.error(request, "special characters not allowed in name")

                    else:
                        messages.error(request, "invalid phone number")
            except Exception as e:
                print(e)
                pass
        
    
    except Exception as e:
            print(e)
            pass
    
    context["phone"] = phone
    context["first_name"] = first_name
    context["password"] = password

    return render(request, 'accounts/signup.html', context)


#login view
def login(request):
    phone  = password = ""
    context = {}
    try:

        #check if user is authenticated
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in")
            return redirect('home')
        else:
            try:
                if request.method == "POST":
                    phone = request.POST.get("phone")
                    password = request.POST.get("password")
                    #check if phone number is valid
                    if phone.isdigit() and len(phone)==10:

                        #check if user exists with given phone number
                        if User.objects.filter(phone = phone).first() is None:
                            messages.error(request, "no account exists with this phone number")
                        else:
                            #authenticate the user
                            auth_user = auth.authenticate(phone = phone, password = password)
                            if auth_user is not None:
                                #login the user
                                auth.login(request, auth_user)
                                
                                phone = password = ""

                                #if next in url then return to that page
                                if request.GET.get('next') != None:
                                    return redirect(request.GET.get('next'))

                                #redirect user to chat page
                                return redirect('home')
                            else:
                                messages.error(request, "invalid credentials")
                       
                    else:
                        messages.error(request, "invalid phone number")

            except Exception as e:
                print(e)
                pass
        
    
    except Exception as e:
        print(e)
        pass

    context["phone"] = phone
    context["password"] = password

    return render(request, 'accounts/login.html', context)



#logout view
@login_required(login_url="/auth/login")
def logout(request):
    if request.session.get('phone'):
        del request.session['phone']
    
    request.user.last_logout = current_time
    request.user.save()
    auth.logout(request)  
    messages.warning(request, "You are logged out now")  
    return redirect('login')



#update last seen
@login_required(login_url="/auth/login")
def last_seen(request):
    try:
        request.user.last_seen = current_time
        request.user.save()

    except Exception as e:
        print(e)
        return JsonResponse(e, safe=False)
    
    return JsonResponse("Done", safe=False)



#user profile/dashboard view
@login_required(login_url="/auth/login")
def profile(request):
    context = {}
    try:
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            email = request.POST.get("email").lower()
            profile_pic = request.FILES.get('profile_pic')

            # remove profile pic if selected
            if request.POST.get('remove-pic'):
                request.user.profile_pic = ""
            
            #updating profile_pic if present
            if request.FILES.get('profile_pic') is not None:
                request.user.profile_pic=profile_pic
            
            #validating & updating first_name
            if first_name == "" or check_str_special(first_name) == True:
                messages.error(request, "invalid first name")
            else:
                request.user.first_name=first_name

            #validating & updating last_name
            if last_name == "" or check_str_special(last_name)==True:
                messages.error(request, "invalid last name")
            else:
                request.user.last_name=last_name

            #validating & updating email
            if not validate_email(email):
                messages.error(request, "invalid email")
            else:
                request.user.email=email

            request.user.save()
    except Exception as e:
        print(e)
        pass

    return render(request, 'accounts/profile.html', context)


#user contact view
@login_required(login_url="/auth/login")
def user_contact(request):
    context = {}
    contacts = None
    try:
        #get user contacts
        contacts = get_user_contacts(request.user)

    except Exception as e:
        print(e)
        pass
    
    context["contacts"] = contacts
    return render(request, 'accounts/contacts.html', context)



#user notifications view
@login_required(login_url="/auth/login")
def notifications(request):
    
    return render(request, 'accounts/notifications.html')


