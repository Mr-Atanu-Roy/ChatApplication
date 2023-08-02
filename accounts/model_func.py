from accounts.models import UserContacts, Notification, FriendRequests
from accounts.utils import cache_get, cache_set

#func to get user contacts
def get_user_contacts(user):
    '''
    Return all friends of user
    '''

    key = f"{user.id}_contacts_list"

    #get the cached data
    cached_data = cache_get(key)

    #check if data is cached
    if cached_data:
        user_contacts = cached_data
    else:
        user_contacts = UserContacts.objects.filter(user=user).first().contacts.all()
        
        #set the cache
        cache_set(key, user_contacts)

    return user_contacts


#func to get user notification
def get_notifications(user):
    '''
    returns all notifications(not friend request) of user
    '''

    try:

        key = f"{user.id}_notification_list"

        #get the cached data
        cached_data = cache_get(key)

        #check if data is cached
        if cached_data:
            notifications = cached_data
        else:
            #get all notifications related to user
            notifications = Notification.objects.filter(notification_for=user)

            #set the cache
            cache_set(key, notifications)


    except Exception as e:
        print(e)
        return None
    
    return notifications


#func to get user friend request
def get_friend_requests(user, type="received"):
    '''
    returns all friend_requests of user
    '''

    try:

        #SEND->get all friend_requests send from user
        if type.lower() == "send":
            key = f"{user.id}_send_friend_requests_list"
            #get the cached data
            cached_data = cache_get(key)

            #check if data is cached
            if cached_data:
                friend_requests = cached_data
            else:
                friend_requests = FriendRequests.objects.filter(request_from=user)
                #cache the data
                cache_set(key, friend_requests)

        #otherwise RECEIVED->get all friend_requests came for user
        else:
            key = f"{user.id}_receive_friend_requests_list"
            #get the cached data
            cached_data = cache_get(key)

             #check if data is cached
            if cached_data:
                friend_requests = cached_data
            else:
                friend_requests = FriendRequests.objects.filter(request_for=user)
                #cache the data
                cache_set(key, friend_requests)


    except Exception as e:
        print(e)
        return None
    
    return friend_requests


