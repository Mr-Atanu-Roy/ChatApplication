from accounts.models import UserContacts


#func to get user contacts
def get_user_contacts(user):
    user_contacts = UserContacts.objects.filter(user=user).first().contacts.all()

    return user_contacts

