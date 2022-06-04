from datetime import datetime, timedelta
from features.tools import data
from collections import Counter
from scipy import stats
from features.tools import get_statistical_results_of_list
import numpy as np

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

def total_days(tweets): #/!\ Not starting with f_ because we don't want to get a feature out of this !!
    first = datetime.strptime(tweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    days = (first-last).days
    return days

def consecutive_days(tweets): #/!\ Not starting with f_ because we don't want to get a feature out of this !!
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    dateList = []
    numofDays = total_days(tweets)
    for n in range(numofDays + 1):
        dateList.append(last.date() + timedelta(n))
    return dateList

def min_max_dates_per_day(tweets): #/!\ Not starting with f_ because we don't want to get a feature out of this !!
    dates = []
    for t in tweets:
        tweet_date = datetime.strptime(t['created_at'],'%a %b %d %H:%M:%S +0000 %Y').date()
        dates.append(tweet_date)
    date_list = consecutive_days(tweets)
    c = Counter(dates)
    if len(date_list)>0:
        for d in date_list:
            if d not in c:
                c[d]=0
        return c
    else:
        return None

def f_total_days(data:data):
    tweets = data.getTweets()
    return total_days(tweets)

def f_total_hours(data:data):
    tweets = data.getTweets()
    first = datetime.strptime(tweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    hours = (first - last).total_seconds()
    return hours

def f_max_min_tweets_per_day(data:data):
    tweets = data.getTweets()
    c = min_max_dates_per_day(tweets)
    if c != None:
        return get_statistical_results_of_list(np.array(list(c.values())).flatten())
               #min(c.values()), max(c.values()), np.mean(list(c.values())), np.median(list(c.values())), np.std(list(c.values())), \
               #stats.skew(list(c.values())), stats.kurtosis(list(c.values())), stats.entropy(list(c.values())),c
    else:
        # print('get_max_min_tweets_per_day')
        return get_statistical_results_of_list([])

def f_consecutive_days_of_no_activity(data:data):
    tweets = data.getTweets()
    c = min_max_dates_per_day(tweets)
    if c == None: return 0
    alldates = consecutive_days(tweets)
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

def f_consecutive_days_of_activity(data:data):
    tweets = data.getTweets()
    c = min_max_dates_per_day(tweets)
    if c == None: return 0
    alldates = consecutive_days(tweets)
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

def f_average_time_between_tweets(data:data):
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

def f_max_occurence_of_same_gap(data:data):
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