from ast import If
import numbers
from xml.dom import UserDataHandler
from tools import data
import re
import datetime

################################################################
# In this script we put all the temporal related features.
# All the functions starting with 'f_' will be called and
# they are expected to return a feature. The feature name is
# defined by the function name excluding the 'f_'.
# In case the feature returns multiple data, put then in a list
# that will contains another list of length two, the first item
# will be an identifier and the second the value.
# Example :
# def f_date(data:data):
#   tweets = data.getTweets()
#   first = datetime.strptime(tweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
#   last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
#   return [ ["first",first] , ["last", last ]  ]
#The example above will create two new features in our dataset, the date_first
#and the date_last.
################################################################

def f_user_id(data:data):
    userData = data.getUserData()
    if not "id_str" in userData: return None
    return userData['id_str']

def f_user_name(data:data):
    userData = data.getUserData()
    if not "name" in userData: return None
    return userData['name']

def f_user_screen_name(data:data):
    userData = data.getUserData()
    if not "screen_name" in userData: return None
    return userData['screen_name']

def f_user_screen_name_length(data:data):
    userData = data.getUserData()
    if not "screen_name" in userData: return None
    return len(userData['screen_name'])

def f_user_followers_count(data:data):
    userData = data.getUserData()        
    if not "followers_count" in userData: return None
    return userData['followers_count']

def f_user_friends_count(data:data):
    userData = data.getUserData()        
    if not "friends_count" in userData: return None
    return userData['friends_count']

def f_user_is_verified(data:data):
    userData = data.getUserData()        
    if not "verified" in userData: return None
    return userData['verified']

def f_user_description_length(data:data):
    userData = data.getUserData()        
    if not "description" in userData: return 0
    return len(userData['description'])

def f_numbers_in_screen_name(data:data):
    userData = data.getUserData()        
    if not "screen_name" in userData: return None
    numbers = re.findall(r'\d+', userData["screen_name"])
    return len(numbers)  

def f_numbers_in_name(data:data):
    userData = data.getUserData()        
    if not "name" in userData: return None
    numbers = re.findall(r'\d+', userData["name"])
    return len(numbers) 

def f_user_tweets_count(data:data):
    userData = data.getUserData()        
    if not "statuses_count" in userData: return None
    return userData['statuses_count']

def f_has_bot_word_in_name(data:data):
    userData = data.getUserData() 
    if not "name" in userData: return None
    matchObj = re.search('bot', userData['name'], flags=re.IGNORECASE)
    if matchObj:
        return True
    else: 
        return False  

def f_has_bot_word_in_screen_name(data:data):
    userData = data.getUserData() 
    if not "screen_name" in userData: return None
    matchObj = re.search('bot', userData['screen_name'], flags=re.IGNORECASE)
    if matchObj:
        return True
    else: 
        return False     

def f_has_bot_word_in_description(data:data):
    userData = data.getUserData() 
    if not "description" in userData: return None
    matchObj = re.search('bot', userData['description'], flags=re.IGNORECASE)
    if matchObj:
        return True
    else: 
        return False      

def f_user_tweets_count(data:data):
    userData = data.getUserData()        
    if not "created_at" in userData: return None
    created_at = datetime.strptime(userData['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    now = datetime.today()
    delta = now-created_at
    return (delta.days)               