import pymongo as mongo
from pandas import DataFrame, concat
from features.features import Features

def getFeaturesFromDBData(mongo_db_uri):
    db = Database(mongo_db_uri)
    i = 0
    dataset = DataFrame()
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
        features = Features(tweets,user)
        features = features.get_all_features()
        features['label'] = label
        df_dictionary = DataFrame([features])
        dataset = concat([dataset, df_dictionary], ignore_index=True)
        i += 1
    return dataset

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