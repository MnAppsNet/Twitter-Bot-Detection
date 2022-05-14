from constants import properties as prop
from inspect import getmembers, isfunction
import user, temporal, content, tools

class features:
    def __init__(self,tweets,user,*otherData):
        self.data = tools.data(tweets,tweets[0][prop.user],user,otherData)

    def get_features(self,importedScript):
        user_features = {}
        for fm in getmembers(importedScript, isfunction):
            if not fm[0][:2] == 'f_': continue
            user_features[fm[0][2:]] = eval(importedScript.__name__ + "." + fm[0] + "(self.data)")
        return user_features

    def get_user_features(self):
        return self.get_features(user)

    def get_temporal_features(self):
        return self.get_features(temporal)

    def get_temporal_features(self):
        return self.get_features(content)

    #################################################################
    # /!\ More feature types can be added here by importing another #
    # /!\ script and implementing a new method to get the features  #
    #################################################################
    # Template :                                                    #
    # def get_***_features(self):                                   #
    #   return self.get_features(***)                               #
    #################################################################
