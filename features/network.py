from datetime import datetime,date,timedelta
import statistics
from itertools import combinations
from features.tools import data


def f_get_average_age_difference_in_retweets(data:data):
    tweets = data.getTweets()
    my_age = datetime.strptime(tweets[0]['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    age_difList=[]
    for t in tweets:
        if 'retweeted_status' in t:
            retweeted_age =datetime.strptime(t['retweeted_status']['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            age_dif = abs((my_age-retweeted_age).days)
            age_difList.append(age_dif)
    if len(age_difList)>0:
        try:
            return statistics.mean(age_difList),statistics.median(age_difList)
        except:
            print('error in get average age difference in retweets')
    else:
        return None,None