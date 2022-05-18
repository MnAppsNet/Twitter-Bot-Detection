from tools import data

################################################################
# In this script we put all the features related to the user
# All the functions starting with 'f_' will be callled and they
# are expected to return a feature
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