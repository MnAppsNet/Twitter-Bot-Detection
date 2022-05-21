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
        return [
            ["min",min(aList)], ["max",max(aList)], ["mean",np.mean(aList)], ["median",np.median(aList)], ["std",np.std(aList)],
            ["skew",stats.skew(aList)], ["kurtosis",stats.kurtosis(aList)], ["entropy",stats.entropy(aList)]
        ]
    else:
        return [
            ["min",0], ["max",0], ["mean",0], ["median",0], ["std",0], ["skew",0], ["kurtosis",0], ["entropy",0]
        ]

def get_all_texts(tweets):
    all_texts=[]
    for t in tweets:
        if 'full_text' in t:
            all_texts.append(t['full_text'])
        else:
            all_texts.append(t['text'])
    return all_texts