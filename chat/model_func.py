from chat.models import Group, ChatMessages

#func to get user group
def get_user_group(user):
    '''
    Returns a list of groups in which user is a member
    '''
    group = []

    #get groups where user is a member
    get_groups = Group.objects.filter(members__in=[user])
    group_len = len(get_groups)

    if(group_len > 0):
        for grp in get_groups:
            group_name = grp.name
            group_pic = grp.group_pic
            group_desc = grp.description
            link = f"/chat/group/{grp.id}"

            #append the data of group in a dict and then in a list
            data = {
                "name": group_name,
                "link": link,
                "group_pic": group_pic,
                "desc": group_desc
            }

            group.append(data)

    return group, group_len


#func to get group messages of group(=Group model instance)
def get_group_messages(group):
    group_msg = ChatMessages.objects.filter(group=group)
    if len(group_msg) == 0:
        group_msg = None

    return group_msg


#func to get user chats: PERSONAL & GROUP based on group name
def get_user_chats(user, group_name=""):

    try:
        chat_groups = Group.objects.filter(members__in=[user], name__icontains=group_name)
        if len(chat_groups) < 1:
            return None
    except Exception as e:
        return None


    return chat_groups



