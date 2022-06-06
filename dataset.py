import pymongo as mongo, numpy as np
from pandas import DataFrame, concat
from features.features import Features

def getFeaturesFromDBData(mongo_db_uri):
    db = Database(mongo_db_uri)
    i = 0
    dataset = DataFrame()
    executionTimes = []
    while True:
        document = db.getDocument(i)
        if not document: break
        if not 'tweets' in document or not 'user' in document:
            i += 1
            continue
        tweets = document['tweets']
        user = document['user']
        label = document['label']
        if len(tweets) == 0:
            print(f'User {user} ({label}) has no tweets in the database')
            i += 1
            continue
        df_dictionary, executionTime = getUserFeaturesFromTweets(tweets,user,label)
        executionTimes.append(executionTime)
        dataset = concat([dataset, df_dictionary], ignore_index=True)
        i += 1
    print("Mean time to extract all features for a user : " + str(np.mean(executionTimes)))
    return dataset

def getUserFeaturesFromTweets(tweets,user,label = None):
   features = Features(tweets,user)
   featuresDict = features.get_all_features()
   if label != None: featuresDict['label'] = label
   return DataFrame([featuresDict]), features.executionTime

class Database:
    def __init__(self,uri):
        self.client = mongo.MongoClient(uri)
        self.database = self.client["tweeter"]
        self.collection = self.database["tweets"]

    def addDocument(self,document):
        '''
        Insert one document in the mongo collection in use
        '''
        #If document exists, replace it else insert it
        self.collection.replace_one({'_id':document['_id']},document,True)

    def getDocument(self,index):
        '''
        Returns all documents saved in the mongo collection
        '''
        #If document exists, replace it else insert it
        return self.collection.find_one({"_id": index})

    def creatIndex(self,index):
        self.collection.create_index(index)