from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from chat.models import Group, ChatMessages
from accounts.models import Notification

from accounts.utils import cache_delete, draft_notification_msg


#signals

@receiver(post_save, sender=Group)
def Group_create_handler(sender, instance, created,  *args, **kwargs):
    '''
    This signal will delete the cached data of user groups list when user creates his groups. It will also notify members about group creation
    '''

    try:
        if created:
            #get all the group members
            members = instance.members.all()

            for user in members:
                #DELETING THE CACHE STORE FOR CHAT BASE
                key = f"{user.id}_groups_list"
                #delete the cache
                cache_delete(key)

                #create notification instance about group creation excluding owner
                if user != instance.owner:
                    new_notification = Notification(
                    notification_type="group", 
                    notification_for = user,
                    message = f"{instance.owner.first_name} {instance.owner.last_name} added you in {instance.name}"
                    )
                    new_notification.save()

    except Exception as e:
        print(e)
        pass


@receiver(pre_save, sender=Group)
def Group_update_delete_handler(sender, instance, *args, **kwargs):
    '''
    This signal will delete the cached data of user groups list when user updates/deletes his groups
    '''

    try:
        #get all the group members
        members = instance.members.all()
        
        for user in members:
            key = f"{user.id}_groups_list"
            #delete the cache
            cache_delete(key)

    except Exception as e:
        print(e)
        pass


@receiver(pre_delete, sender=Group)
def Group_delete_handler(sender, instance, *args, **kwargs):
    '''
    This signal will delete the cached data of user groups list when user deletes his groups
    '''
    
    try:
        #get all the group members
        members = instance.members.all()

        for user in members:
            #DELETING THE CACHE STORE FOR CHAT BASE
            key = f"{user.id}_groups_list"
            #delete the cache
            cache_delete(key)

    except Exception as e:
        print(e)
        pass


@receiver(post_save, sender=ChatMessages)
def ChatMessages_create_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will delete the cached data of group message list when new message is created or updated. It will also send notification to its group member about the upload
    '''
    
    try:
       #delete cache when new msg is created or old msg is updated
       key = f"{instance.group.id}_chat_messages"
       cache_delete(key)

       #send notification when new instance is created
       if created:
        #getting group members
        group_members = instance.group.members.all()
        
        #send notification to each member excluding sender
        for member in group_members:

            #check if member is not sender
            if member != instance.sender:
                #getting notification msg
                notification_message = draft_notification_msg(instance)

                #create a notification instance
                new_notification = Notification(
                    notification_type=instance.group.type, 
                    notification_for = member,
                    message = notification_message
                )
                new_notification.save()

    except Exception as e:
        print(e)
        pass


@receiver(pre_delete, sender=ChatMessages)
def ChatMessages_delete_handler(sender, instance, *args, **kwargs):
    '''
    This signal will delete the cached data of group message list when new message is deleted
    '''
    
    try:
       key = f"{instance.group.id}_chat_messages"
       cache_delete(key)

    except Exception as e:
        print(e)
        pass







