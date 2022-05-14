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