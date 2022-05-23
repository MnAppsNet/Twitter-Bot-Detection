from datetime import datetime
import statistics
from itertools import combinations
from features.tools import data
import networkx as nx


def f_get_average_age_difference_in_retweets(data:data):
    tweets = data.getTweets()
    my_age = datetime.strptime(tweets[0]['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    age_difList=[]
    for t in tweets:
        if 'retweeted_status' in t:
            retweeted_age =datetime.strptime(t['retweeted_status']['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            age_dif = abs((my_age-retweeted_age).days)
            age_difList.append(age_dif)
    if len(age_difList)>0:
        try:
            return statistics.mean(age_difList),statistics.median(age_difList)
        except:
            print('error in get average age difference in retweets')
    else:
        return None,None

def f_get_network_of_retweeters(retweets,neighbor_tweets):
    user = retweets[0]['user']['id_str']
    G = nx.Graph()
    for t in retweets:
        retweeter = t['retweeted_status']['user']['id_str']
        G.add_edge(user,retweeter)
    for n in neighbor_tweets:
        neighbor = n['user']['id_str']
        entities = n['entities']
        for i in entities['user_mentions']:
            G.add_edge(neighbor,i)
    print (nx.info(G))
    return G,user

def f_graph_features(G):
    try:
        density = nx.density(G)
        avg_clustering = nx.average_clustering(G)
        triangles = nx.triangles(G)
        # betweeness = nx.betweenness_centrality(G)[user]
        # closeness = nx.closeness_centrality(G,wf_improved = True)[user]
        # pagerank = nx.pagerank(G,alpha=0.85)[user]
        # voterank = nx.voterank(G).index(user)
        volume = G.number_of_nodes()
        mass = G.number_of_edges()
    except ZeroDivisionError:
        return 0,0,[],0,0
    return density,avg_clustering,triangles,volume,mass

def f_hashtag_network(data:data):
    tweets = data.getTweets()
    G = nx.Graph()
    for t in tweets:
        entities = t['entities']
        tags = entities['hashtags']
        hashtags = set()
        for i in tags:
            hashtags.add(i['text'])
        G.add_nodes_from(hashtags)
        if len(hashtags)>1:
            combis = combinations(hashtags,2)
            for c in combis:
                # print (c)
                if G.has_edge(c[0],c[1]):
                    G[c[0]][c[1]]['weight']+=1.0
                else:
                    G.add_edge(c[0],c[1],weight=1.0)
    allweights=[x[2]['weight'] for x in G.edges(data=True)]
    return G,allweights