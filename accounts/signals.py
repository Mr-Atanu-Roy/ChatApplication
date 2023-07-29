from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, UserContacts

from accounts.utils import cache_delete


#signals

@receiver(post_save, sender=User)
def User_created_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will be executed each time a new user is created. It will add a UserContacts instance
    '''

    try:
        #execute only if db record is created
        if created:    
            user_contact = UserContacts(user=instance)
            user_contact.save()

    except Exception as e:
        print(e)
        pass


@receiver(post_save, sender=UserContacts)
def UserContact_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will delete the cached data of user contacts when user updates his contact
    '''

    try:
        
        key = f"{instance.user.id}_contacts_list"
        #delete the cache
        cache_delete(key)

    except Exception as e:
        print(e)
        pass