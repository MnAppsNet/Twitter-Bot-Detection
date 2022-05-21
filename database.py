import pymongo as mongo

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