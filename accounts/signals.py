from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, UserContacts, Notification, FriendRequests

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



@receiver(post_save, sender=FriendRequests)
def FriendRequest_create_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will add a notification instance whenever someone sends a friend request
    '''

    #execute only when instance is created
    if created:
        #create a notification instance
        new_notification = Notification(
            notification_type="personal", 
            notification_for = instance.request_for,
            message = f"You have a new friend request from: {instance.request_from}"
        )
        new_notification.save()



@receiver(post_save, sender=FriendRequests)
def FriendRequest_accept_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will add the contact to users contact if the user accepts the friend request. It will also send a notification to user who send the friend request
    '''


    #execute only when instance is updated
    if not created:
        #check if friend request is accepted
        if instance.status == True:
            #get the contact instance of both users
            user1_contact = UserContacts.objects.filter(user = instance.request_for).first()
            user2_contact = UserContacts.objects.filter(user = instance.request_from).first()

            #check if both user has contact instance
            if user1_contact is not None and user2_contact is not None:
                #add each other to each other contacts
                user1_contact.contacts.add(instance.request_from)
                user1_contact.save()
                user2_contact.contacts.add(instance.request_for)
                user2_contact.save()

                #send notification to inform the user
                new_notification = Notification(
                    notification_type="personal", 
                    notification_for = instance.request_from,
                    message = f"{instance.request_for} accepted your friend request. You both are now friends",
                )
                new_notification.save()



