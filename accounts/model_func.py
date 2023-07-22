from accounts.models import UserContacts
from accounts.utils import cache_get, cache_set

#func to get user contacts
def get_user_contacts(user):

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

