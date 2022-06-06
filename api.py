import tweepy, json
from dataset import Database

class API:
    def __init__(self):
        try:
            keyFile = open('api_key.json')
            self.key = json.load(keyFile)
            keyFile.close()
        except:
            raise "Create a JSON file 'api_key.json' with the tweeter API keys, that contains the properties 'key', 'key_secret', 'token' and 'token_secret'."
        auth = tweepy.OAuthHandler(consumer_key=self.key['key'], consumer_secret=self.key['key_secret'])
        auth.set_access_token(self.key['token'], self.key['token_secret'])
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def getUserTimelineFromTwitter(self, userID):
        return self.api.user_timeline(user_id=str(userID),count=200,tweet_mode="extended",wait_on_rate_limit=True)

    def getUserListTimelineFromTwitter(self, userIDs:list):
        tweets = {}
        for userID in userIDs:
            tweets[userID] = self.api.user_timeline(user_id=str(userID),count=200,tweet_mode="extended",wait_on_rate_limit=True)
        return tweets

    def getDataFromTweeterInDB(self, mongo_database_uri,users_csv):
        db = Database(mongo_database_uri)
        user_ids = open(users_csv)
        lines = user_ids.readlines()
        user_ids.close()
        users = {}
        for line in lines:
            user_id = line.split(',')[0]
            label = line.split(',')[1].replace('\n','')
            if not label in users:
                users[label] = []
            users[label].append(user_id)

        max_users = 2500
        i = 0
        bots = 0
        humans = 0

        while i < max_users:
            if i%2 == 0:
                label = 'BOT'
                index = bots
                bots += 1
            else:
                label = 'HUMAN'
                index = humans
                humans += 1

            try:
                user_id = users[label][index]
            except:
                try:
                    if label == 'BOT':
                        user_id = users['HUMAN'][humans]
                        humans += 1
                    else:
                        user_id = users['BOT'][bots]
                        bots += 1
                except:
                    user_id = None

            if user_id == None:
                break
            print(f"{str(i)}. Fetching tweets of user {str(user_id)} ({str(label)})")
            try :
                tweets = self.getUserTimelineFromTwitter(str(user_id))
            except Exception as e:
                print(e)
                tweets = None

            if tweets == None:
                if label == 'BOT': bots += 1
                elif label == 'HUMAN': humans += 1
                continue

            tweet_list = []
            for t in tweets:
                tweet_list.append(t._json)
            db.addDocument(
                {
                    "_id": i,
                    "user":str(user_id),
                    "label": label,
                    "tweets":tweet_list
                }
            )
            i += 1
        print("Data fetching completed!")