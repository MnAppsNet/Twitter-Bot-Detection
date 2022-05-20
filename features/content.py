import math
from tools import data
from features.tools import get_all_texts, get_statistical_results_of_list, get_retweets
from twitter_preprocessor import TwitterPreprocessor
from itertools import combinations
from nltk import pos_tag, word_tokenize
import string
from collections import Counter

################################################################
# In this script we put all the features related to the content
# of the tweets. All the functions starting with 'f_' will be
# callled and they are expected to return a feature
################################################################

def calculate_entropy(sentence):
    entropy = 0
    # There are 256 possible ASCII characters
    for character_i in range(256):
        Px = sentence.count(chr(character_i)) / len(sentence)
        if Px > 0:
            entropy += - Px * math.log(Px, 2)
    return entropy

def f_text_size_distributions(data:data):
    tweets = data.getTweets()
    length=[]
    for t in tweets:
        if 'retweeted_status' not in t:
            try:
                text = t['full_text']
            except KeyError:
                text = t['text']
            p = TwitterPreprocessor(text)
            p.partially_preprocess()
            new = p.text
            numOfWords = len(new.split())
            length.append(numOfWords)
    return get_statistical_results_of_list(length)

def f_text_entropy_distributions(data:data):
    tweets = data.getTweets()
    texts = []
    for t in tweets:
        if 'retweeted_status' not in t:
            try:
                text = t['full_text']
            except KeyError:
                text = t['text']
            p = TwitterPreprocessor(text)
            p.partially_preprocess()
            new = p.text
            texts.append(text)
    entropies= []
    for t in texts:
        ent = calculate_entropy(t)
        entropies.append(ent)
    return get_statistical_results_of_list(entropies)

def f_jaccard_sim(str1, str2):
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
            similarities.append(f_jaccard_sim(c[0], c[1]))
    return get_statistical_results_of_list(similarities)

def f_total_pos_tags(data:data):
    tweets = data.getTweets()
    texts = get_all_texts(tweets)
    allTags=[]
    for t in texts:
        p = TwitterPreprocessor(t)
        p.pos_tag_preprocess()
        new = p.text
        text = word_tokenize(new)
        tags = [i[1] for i in pos_tag(text)]
        allTags.extend(tags)
    return allTags

def f_pos_tag_per_tweet(data:data):
    tweets = data.getTweets()
    texts = get_all_texts(tweets)
    perTweetTags=[]
    for t in texts:
        p = TwitterPreprocessor(t)
        p.pos_tag_preprocess()
        new = p.text
        text = word_tokenize(new)
        tags = [i[1] for i in pos_tag(text)]
        perTweetTags.append(tags)
    return perTweetTags

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

def f_marks_distribution(tweets):
    marksPerTweet = f_marks_per_tweet(tweets)
    return get_statistical_results_of_list(marksPerTweet)