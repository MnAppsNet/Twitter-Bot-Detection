from datetime import datetime, timedelta
from tools import data
from collections import Counter
from scipy import stats
from features.tools import get_statistical_results_of_list
import numpy as np

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

def f_consecutive_days(data:data):
    tweets = data.getTweets()
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    dateList = []
    numofDays = f_total_days(tweets)
    for n in range(numofDays + 1):
        dateList.append(last.date() + timedelta(n))
    return dateList

def f_get_max_min_tweets_per_day(data:data):    
    tweets = data.getTweets()
    dates = []
    for t in tweets:
        tweet_date = datetime.strptime(t['created_at'],'%a %b %d %H:%M:%S +0000 %Y').date()
        dates.append(tweet_date)
    date_list = f_consecutive_days(tweets)
    # print (date_list)
    c = Counter(dates)
    if len(date_list)>0:
        for d in date_list:
            if d not in c:
                c[d]=0
        # print (c.values())
        return min(c.values()), max(c.values()), np.mean(list(c.values())), np.median(list(c.values())), np.std(list(c.values())), \
               stats.skew(list(c.values())), stats.kurtosis(list(c.values())), stats.entropy(list(c.values())),c
    else:
        # print('get_max_min_tweets_per_day')
        return 0,0,0,0,0,0,0,0,c    

def f_get_consecutive_days_of_no_activity(data:data):
    tweets = data.getTweets()
    minV, maxV, meanV, medianV, stdV, \
    skewV, kurtV, entV, c= f_get_max_min_tweets_per_day(tweets)
    alldates = f_consecutive_days(tweets)
    i = 0
    maximum = 0
    dat = []
    if len(alldates) > 0:
        for d in alldates:
           if c[d]==0:
               dat.append(d)
               i+=1
           else:
               if i > maximum:
                   maximum = i
               i=0
        if maximum == 0:
            maximum = i
        # print ('maximun days of no activity',maximum)
        # print (dat)
        return maximum
    else:
        return 0    

def f_get_consecutive_days_of_activity(data:data):
    tweets = data.getTweets()
    # print ('get_consecutive_days_of_activity')
    minV, maxV, meanV, medianV, stdV, \
    skewV, kurtV, entV, c = f_get_max_min_tweets_per_day(tweets)
    alldates = f_consecutive_days(tweets)
    i = 0
    maximum = 0
    dat = []
    if len(alldates) > 0:
        for d in alldates:
           if c[d]>0:
               dat.append(d)
               i+=1
           else:
               if i > maximum:
                   maximum = i
               i=0
        if maximum == 0:
            maximum = i
        # print ('maximum days of activity',maximum)
        # print (dat)
        return maximum
    else:
        return maximum           

def f_get_average_time_between_tweets(data:data):
    tweets = data.getTweets()    
    # print ('get average time between tweets')
    gapList = []
    for i in range(0, len(tweets) - 1):
        first = datetime.strptime(tweets[i]['created_at'],
                                  '%a %b %d %H:%M:%S +0000 %Y')
        second = datetime.strptime(tweets[i + 1]['created_at'],
                                   '%a %b %d %H:%M:%S +0000 %Y')
        gap = ((first - second).seconds)
        gapList.append(gap)
    return get_statistical_results_of_list(gapList)      

def f_get_max_occurence_of_same_gap(data:data):
    tweets = data.getTweets()     
    # print ('get average time between tweets')
    gapList = []
    if len(tweets) > 2:
        for i in range(0, len(tweets) - 1):
            first = datetime.strptime(tweets[i]['created_at'],
                                      '%a %b %d %H:%M:%S +0000 %Y')
            second = datetime.strptime(tweets[i + 1]['created_at'],
                                       '%a %b %d %H:%M:%S +0000 %Y')
            gap = ((first - second).seconds)
            gapList.append(gap)
        c = Counter(gapList)
        # print (gapList)
        max_occ = c.most_common(1)[0][1]
    else:
        max_occ = 0
    return max_occ       