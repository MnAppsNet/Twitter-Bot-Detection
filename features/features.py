from features.constants import properties as prop
from inspect import getmembers, isfunction
import features.user, features.temporal, features.tools as tools#, features.content

class Features:
    def __init__(self,tweets,user,*otherData):
        self.data = tools.data(tweets,tweets[0][prop.tweet.USER],user,otherData)

    def get_features(self,importedScript):
        user_features = {}
        for fm in getmembers(importedScript, isfunction):
            if not fm[0][:2] == 'f_': continue
            results = eval(importedScript.__name__ + "." + fm[0] + "(self.data)")
            feature_name = fm[0][2:]
            if type(results) == list:
            #If a list of features is returned, create a new entry for each
                if len(results) >= 2:
                    for result in results:
                        user_features[feature_name + str(results[0])] = result[1]
            else:
                user_features[feature_name] = results
        return user_features

    def get_user_features(self):
        return self.get_features(features.user)

    def get_temporal_features(self):
        return self.get_features(features.temporal)

    def get_content_features(self):
        return self.get_features(features.content)
    
    def get_network_features(self):
        return self.get_features(features.network)
    
    def get_sentiment_features(self):
        return self.get_features(features.sentiment)

    #################################################################
    # /!\ More feature types can be added here by importing another #
    # /!\ script and implementing a new method to get the features  #
    #################################################################
    # Template :                                                    #
    # def get_***_features(self):                                   #
    #   return self.get_features(***)                               #
    #################################################################
