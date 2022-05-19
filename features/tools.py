import scipy.stats as stats
import numpy as np
from scipy.special import entr

class data:
    def __init__(self,tweets,userData,user, *otherData):
        self.tweets = tweets
        self.userData = userData
        self.user = user
        self.otherData = []
        for other in otherData:
            self.otherData.append(other)

    def getTweets(self): return self.tweets
    def getUserData(self): return self.userData
    def getUser(self): return self.user


def get_statistical_results_of_list(aList):
    if len(aList)>=1:
        return min(aList), max(aList), np.mean(aList), np.median(aList), np.std(aList), \
               stats.skew(aList), stats.kurtosis(aList), entr(np.array(aList)).sum()
    else:
        return 0,0,0,0,0,0,0,0

def get_all_texts(tweets):
    all_texts=[]
    for t in tweets:
        if 'full_text' in t:
            all_texts.append(t['full_text'])
        else:
            all_texts.append(t['text'])
    return all_texts