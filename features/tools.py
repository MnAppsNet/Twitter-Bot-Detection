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


def get_statistical_results_of_list(aList, name):
    if len(aList)>=1:
        return [
            [name+" min",min(aList)], [name+" max",max(aList)], [name+" mean",np.mean(aList)], [name+" median",np.median(aList)], [name+" std",np.std(aList)],
            [name+" skew",stats.skew(aList)], [name+" kurtosis",stats.kurtosis(aList)], [name+" entropy",stats.entropy(aList)]
        ]
    else:
        return [ 
            [name+" min",0], [name+" max",0], [name+" mean",0], [name+" median",0], [name+" std",0], [name+" skew",0], [name+" kurtosis",0], [name+" entropy",0]
        ]

def get_all_texts(tweets):
    all_texts=[]
    for t in tweets:
        if 'full_text' in t:
            all_texts.append(t['full_text'])
        else:
            all_texts.append(t['text'])
    return all_texts