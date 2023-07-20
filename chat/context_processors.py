from chat.model_func import get_user_group

def user_chat_groups_details(request):
    context = {}
    group = []
    group_len = 0
    try:
        if request.user.is_authenticated:
            group, group_len = get_user_group(request.user)      
    except Exception as e:
        print(e)
        pass

    context["group_len"] = group_len
    context["groups"] = group

    return context