import pymongo as mongo

class Database:
    def __init__(self,uri):
        try:
            passwordFile = open('pass.txt')
            password = passwordFile.readline()
            passwordFile.close()
        except:
            raise "Create a file pass.txt with the mongoDB password"
        self.client = mongo.MongoClient(uri)
        self.database = self.client["tweeter"]
        self.collection = self.database["tweets"]

    def addDocument(self,document):
        '''
        Insert one document in the mongo collection in use
        '''
        #If document exists, replace it else insert it
        self.collection.replace_one({'_id':document['_id']},document,True)

    def creatIndex(self,index):
        self.collection.create_index(index)