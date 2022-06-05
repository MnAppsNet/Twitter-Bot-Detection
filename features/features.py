from features.constants import properties as prop
from inspect import getmembers, isfunction
import features.user, features.temporal, features.content, features.sentiment, features.network, features.tools as tools

class Features:
    def __init__(self,tweets,user,*otherData):
        self.data = tools.data(tweets,tweets[0][prop.tweet.USER],user,otherData)

    def get_features(self,importedScript):
        user_features = {}
        for fm in getmembers(importedScript, isfunction):
            if not fm[0][:2] == 'f_': continue
            try:
                results = eval(importedScript.__name__ + "." + fm[0] + "(self.data)")
                feature_name = fm[0][2:]
                if type(results) == list:
                #If a list of features is returned, create a new entry for each
                    if len(results) >= 2:
                        for result in results:
                            if result[1] == None: result[1] = 0
                            if type(result[1]) == str or type(result[1]) == tuple or type(result[1]) == dict:
                                raise Exception(f"Value returned from feature function '{importedScript.__name__}.{fm[0]}', is not numeric")
                            user_features[feature_name + str(result[0])] = result[1]
                elif results == None:
                    user_features[feature_name + str(result[0])] = 0
                elif type(results) == str or type(results) == tuple or type(results) == dict:
                    raise Exception(f"Value returned from feature function '{importedScript.__name__}.{fm[0]}', is not numeric")
                else:
                    user_features[feature_name] = results
            except Exception as ex:
                print(f"An error occurred in feature function '{importedScript.__name__}.{fm[0]}'");
                raise ex;
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

    def get_all_features(self):
        return {
            **self.get_user_features(),
            **self.get_temporal_features()
            **self.get_sentiment_features(),
            **self.get_content_features(),
            **self.get_network_features()
            #/!\ Add more feature to be returned here /!\
            }

    #################################################################
    # /!\ More feature types can be added here by importing another #
    # /!\ script and implementing a new method to get the features  #
    #################################################################
    # Template :                                                    #
    # def get_***_features(self):                                   #
    #   return self.get_features(***)                               #
    #################################################################
