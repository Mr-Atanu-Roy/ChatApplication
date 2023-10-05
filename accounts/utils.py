from django.db import models
from django.conf import settings

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache

from django.contrib.humanize.templatetags import humanize

import uuid
import datetime
import pytz
import re

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

special_char_regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

# Get the timezone object for the timezone specified in settings.py
tz = pytz.timezone(settings.TIME_ZONE)

# Get the current time in the timezone
current_time = datetime.datetime.now(tz)

#func to humanize date
def humanize_date(date_time, date_only=False):
    '''
    This func will humanize the given date-time. If date is smaller than 2 days it returns yesterday. If date_only=True then it will return only date
    '''

    date = date_time.strftime("%d.%m.%Y, %I:%M %p")
    try:

        one_day_ago = current_time - datetime.timedelta(days=1)
        two_days_ago = current_time - datetime.timedelta(days=2)

        if date_time < one_day_ago and date_time > two_days_ago:
            date = "yesterday"
        
        elif date_time > one_day_ago:
            date = humanize.naturaltime(date_time)
        
        else:
            if date_only == True:
                date = date_time.strftime("%d.%m.%Y")
            else:
                date = date_time.strftime("%d.%m.%Y, %I:%M %p")
        

    except Exception as e:
        print(e)

    return date


#base/abstract model for other models
class BaseModel(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


#func to check is a str contains special chars
def check_str_special(string):
    if special_char_regex.search(string):
        return True
    else:
        return False
    

#func to validate email
def validate_email(email):
    validator = EmailValidator()

    try:
        validator(email)
    except ValidationError:
        return False

    return True


#func to check weather key was cached
def cache_get(key):
    '''
    this will return the cached data if its present in cache, None otherwise
    '''

    return cache.get(key)


#func to set cache
def cache_set(key, value, ttl_sec=CACHE_TTL):
    '''
    this will cache the value with key
    '''
    
    cache.set(key, value, timeout=ttl_sec)


#func to delete cache
def cache_delete(key):
    '''
    this will delete cache data with key
    '''
    
    cache.delete(key)

#func to delete cache with given prefix
def cache_delete_many(key_with_prefix):
    '''
    this will delete cache data with key prefix key_with_prefix
    '''
    
    cache.delete_many(keys=key_with_prefix)


#func to get or create cache data
def cache_get_or_create(key, value="", ttl_sec=CACHE_TTL):
    '''
    this will return the cache data with key if present else it will cache the data with key and value. Return type: cached data, Bool. Bool indicating if data is cached now
    '''
    
    cached_data = cache_get(key)
    #check if cached data exists
    if cached_data:
        return cached_data, False
    
    #set the cache 
    cache_set(key, value, ttl_sec)

    #get and return the cache
    return cache_get(key), True


VALID_EXTENSIONS = {
    "img": ['png', 'gif', 'jpg', 'jpeg'],
    "doc": ['doc', 'docx', 'ppt', 'pptx', 'pdf'],
    "audio":  ['mp3', 'ogg'],
    "video": ['mp4', 'mov'],
}


#func to check file type from extension
def get_file_type(ext):
    
    for ext_types in VALID_EXTENSIONS:
        if ext in VALID_EXTENSIONS.get(ext_types):
            return ext_types
            
    
    return None


#func to generate notification message based on group type
def draft_notification_msg(instance):
    msg = f"{instance.sender.first_name} {instance.sender.last_name}"

    #check the group type
    if instance.group.type == "personal":
        msg += " send a new "
        #check the message type
        if instance.message_type == "image":
            msg += "image"
        elif instance.message_type == "video":
            msg += "video"
        elif instance.message_type == "audio":
            msg += "audio message"
        elif instance.message_type == "doc":
            msg += "new document"
        else:
            msg += "message"
        msg += " to you"
    else:
        msg += " uploaded a new "
        #check the message type
        if instance.message_type == "image":
            msg += "image"
        elif instance.message_type == "video":
            msg += "video"
        elif instance.message_type == "audio":
            msg += "audio message"
        elif instance.message_type == "doc":
            msg += "new document"
        else:
            msg += "message"
        msg += f" in {instance.group.name} Group"

    return msg

