from database import Database
from pandas import DataFrame, concat
from features.features import Features

def getFeatures(mongo_db_uri):
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
        user_features = features.get_user_features()
        temporal_features = features.get_temporal_features()
        features = {**user_features,**temporal_features}
        features['label'] = label
        df_dictionary = DataFrame([features])
        dataset = concat([dataset, df_dictionary], ignore_index=True)
        i += 1
    return dataset