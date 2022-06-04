import math
from features.tools import data
from features.tools import get_all_texts, get_statistical_results_of_list
from itertools import combinations
from nltk import pos_tag, word_tokenize
import string
from collections import Counter

################################################################
# In this script we put all the temporal related features.
# All the functions starting with 'f_' will be called and
# they are expected to return a feature. The feature name is
# defined by the function name excluding the 'f_'.
# In case the feature returns multiple data, put then in a list
# that will contains another list of length two, the first item
# will be an identifier and the second the value.
# Example :
# def f_date(data:data):
#   tweets = data.getTweets()
#   first = datetime.strptime(tweets[0]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
#   last = datetime.strptime(tweets[-1]['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
#   return [ ["first",first] , ["last", last ]  ]
#The example above will create two new features in our dataset, the date_first
#and the date_last.
################################################################

def jaccard_sim(str1, str2): #/!\ Not starting with f_ because we don't want to get a feature out of this !!
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    try:
        return float(len(c)) / (len(a) + len(b) - len(c))
    except ZeroDivisionError:
        return 0.0

def f_similarities(data:data):
    tweets = data.getTweets()
    texts = get_all_texts(tweets)
    similarities = []
    if len(texts)>2:
        combos = combinations(texts, 2)
        for c in combos:
            similarities.append(jaccard_sim(c[0], c[1]))
    return get_statistical_results_of_list(similarities, "similarities")

def f_all_punctuation_marks(data:data):
    tweets = data.getTweets()
    marks=[]
    all_texts = get_all_texts(tweets)
    for t in all_texts:
        marks.extend([char for char in t if char in string.punctuation])
    return marks


def f_common_marks(data:data):
    tweets = data.getTweets()
    allmarks = f_all_punctuation_marks(tweets)
    if len(allmarks) > 0:
        c = Counter(allmarks)
        return c.most_common(1)[0][0],c.most_common(1)[0][1]
    else:
        return '',0

def f_marks_per_tweet(data:data):
    tweets = data.getTweets()
    marks_count=[]
    all_texts = get_all_texts(tweets)
    if len(all_texts)>2:
        for t in all_texts:
            marks_count.append(len([char for char in t if char in string.punctuation]))
    return marks_count

def f_marks_distribution(data:data):
    tweets = data.getTweets()
    marksPerTweet = f_marks_per_tweet(tweets)
    return get_statistical_results_of_list(marksPerTweet, "marks")

def f_tweet_retweet_ratio(data:data):
    tweets = data.getTweets()
    ts = 0
    rts = 0
    for t in tweets:
        if 'retweeted_status' in t:
            rts += 1
        else:
            ts += 1
    if rts == 0:
        rts += 1
    ratio = ts / (rts)
    return ratio

def source_change(data:data):
    tweets = data.getTweets()
    sourceSet = set()
    for t in tweets:
        source = t['source']
        sourceSet.add(source)
    if len(sourceSet) > 1:
        return True
    else:
        return False

def f_number_of_source(data:data):
    tweets = data.getTweets()
    sourceSet = set()
    for t in tweets:
        source = t['source']
        sourceSet.add(source)
    return len(sourceSet)

def f_unique_mentions_rate(data:data):
    tweets = data.getTweets()
    mentions = set()
    for t in tweets:
        if 'retweeted_status' not in t:
            entities = t['entities']
            for i in entities['user_mentions']:
                mentions.add(i['id_str'])
    return round(len(mentions)/len(tweets),3)

def get_average_marked_as_favorite(data:data):
    tweets = data.getTweets()
    favs = []
    for t in tweets:
        favs.append(t['favorite_count'])
    return get_statistical_results_of_list(favs, "marked as favovorite")

def get_retweeted(data:data):
    tweets = data.getTweets()
    rts = []
    for t in tweets:
        if 'retweeted_status' not in t:
            rts.append(t['retweet_count'])
    return get_statistical_results_of_list(rts, "retweets_per_tweet")

def get_statistics_of_their_retweets(data:data):
    tweets = data.getTweets()
    rts=[]
    for t in tweets:
        if 'retweeted_status' in t:
            times_retweeted = t['retweeted_status']['retweet_count']
            rts.append(times_retweeted)
    return get_statistical_results_of_list(rts, "retweets_stat")