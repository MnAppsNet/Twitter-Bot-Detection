import tweepy, json
from database import Database

keyFile = open('api_key.json')
key = json.load(keyFile)
keyFile.close()

auth = tweepy.OAuthHandler(consumer_key=key['key'], consumer_secret=key['key_secret'])
auth.set_access_token(key['token'], key['token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)

db = Database("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
user_ids = open('users_dataset.csv')
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
      tweets = api.user_timeline(user_id=str(user_id),count=200,tweet_mode="extended",wait_on_rate_limit=True)
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
         "_id": user_id,
         "label": label,
         "tweets":tweet_list
      }
   )
   i += 1

print("Data fetching completed!")