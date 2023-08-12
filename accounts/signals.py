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
def FriendRequest_create_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will add a notification instance whenever someone sends a friend request 
    
    It will also add the contact to users contact if the user accepts the friend request and will send a notification to user who send the friend request
    '''


    if created:
        #if created then delete send_friend_request cache of request_from user and receive_friend_request cache of request_for

        cache_delete(f"{instance.request_from.id}_send_friend_requests_list")
        cache_delete(f"{instance.request_for.id}_receive_friend_requests_list")

        #updating message field
        msg = f"You have a new friend request from: {instance.request_for.first_name} {instance.request_for.last_name}"

        #create a notification instance
        new_notification = Notification(
            notification_type="personal", 
            notification_for = instance.request_for,
            message = msg
        )
        new_notification.save()
        

    #execute when instance is updated
    else:
        #if updated then delete receive_friend_request cache of request_from user and send_friend_request cache of request_for

        cache_delete(f"{instance.request_for.id}_send_friend_requests_list")
        cache_delete(f"{instance.request_from.id}_receive_friend_requests_list")


        #adding to friend list
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
                    message = f"{instance.request_for.first_name} {instance.request_for.last_name} accepted your friend request. You both are now friends",
                )
                new_notification.save()




@receiver(post_save, sender=Notification)
def Notification_create_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will each time a new notification is created/updated delete the notification cache of user for whom the notification has came
    '''

    cache_delete(f"{instance.notification_for.id}_notification_list")

