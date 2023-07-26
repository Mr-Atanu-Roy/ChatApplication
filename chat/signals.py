from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from chat.models import Group, ChatMessages

from accounts.utils import cache_delete, cache_delete_many


#signals

@receiver(post_save, sender=Group)
def Group_create_handler(sender, instance, created,  *args, **kwargs):
    '''
    This signal will delete the cached data of user groups list when user creates his groups
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

                #DELETING CACHE STORED BY SEARCH CHAT API
                cache_delete_many(keys=f"{user.id}_chat_searched_*")

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

            #DELETING CACHE STORED BY SEARCH CHAT API
            cache_delete_many(keys=f"{user.id}_chat_searched_*")

    except Exception as e:
        print(e)
        pass


@receiver(post_save, sender=ChatMessages)
def ChatMessages_create_update_handler(sender, instance, created, *args, **kwargs):
    '''
    This signal will delete the cached data of group message list when new message is created or updated
    '''
    
    try:
       key = f"{instance.group.id}_chat_messages"
       cache_delete(key)

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



