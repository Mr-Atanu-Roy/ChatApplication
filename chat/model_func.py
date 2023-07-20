from chat.models import Group

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