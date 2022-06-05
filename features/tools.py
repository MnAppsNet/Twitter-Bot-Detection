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
            ["_min",min(aList)], ["_max",max(aList)], ["_mean",np.mean(aList)], ["_median",np.median(aList)], ["_std",np.std(aList)],
            ["_skew",stats.skew(aList)], ["_kurtosis",stats.kurtosis(aList)], ["_entropy",stats.entropy(aList)]
        ]
    else:
        return [
            ["_min",0.0], ["_max",0.0], ["_mean",0.0], ["_median",0.0], ["_std",0.0], ["_skew",0.0], ["_kurtosis",0.0], ["_entropy",0.0]
        ]

def get_all_texts(tweets):
    all_texts=[]
    for t in tweets:
        if 'full_text' in t:
            all_texts.append(t['full_text'])
        else:
            all_texts.append(t['text'])
    return all_texts