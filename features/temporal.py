from datetime import datetime, timedelta
from tools import data

################################################################
# In this script we put all the temporal related features.
# All the functions starting with 'f_' will be callled and
# they are expected to return a feature
################################################################

def f_total_days(data:data):
    tweets = data.getTweets()
    first = datetime.strptime(tweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    days = (first-last).days
    return days

def f_total_hours(data:data):
    tweets = data.getTweets()
    first = datetime.strptime(tweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    hours = (first - last).total_seconds()
    return hours

def get_consecutive_days(data:data): 
    tweets = data.getTweets()
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    dateList = []
    numofDays = f_total_days(tweets)
    for n in range(numofDays + 1):
        dateList.append(last.date() + timedelta(n))
    return dateList