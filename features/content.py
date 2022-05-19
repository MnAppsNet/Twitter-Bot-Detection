import math
from tools import data
from features.tools import get_all_texts, get_statistical_results_of_list, get_retweets
from twitter_preprocessor import TwitterPreprocessor

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

def f_get_text_size_distributions(tweets):
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

def f_get_text_entropy_distributions(tweets):
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