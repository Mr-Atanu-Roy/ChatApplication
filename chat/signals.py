from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from chat.models import Group, ChatMessages

from accounts.utils import cache_delete


#signals

@receiver(post_delete, sender=Group)
@receiver(post_save, sender=Group)
def Group_create_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will delete the cached data of user groups list when user updates his groups
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


@receiver(post_delete, sender=ChatMessages)
@receiver(post_save, sender=ChatMessages)
def ChatMessages_create_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will delete the cached data of group message list when new message is created or deleted or updated
    '''
    
    try:
       key = f"{instance.group.id}_chat_messages"
       cache_delete(key)

    except Exception as e:
        print(e)
        pass



