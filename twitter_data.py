# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:04:29 2017

@author: Louie.Wong
"""

import tweepy
import pandas as pd
import numpy as np
from textblob import TextBlob
from twitter_credentials import * 

# API's setup:
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

# Create an extractor object:
extractor = twitter_setup()

# Create a tweet list as follows:
#cnn
#realDonaldTrump
#HillaryClinton
#notderb
user = 'realDonaldTrump'
trumptweets = tweepy.Cursor(extractor.user_timeline, screen_name='@'+ user, tweet_mode = 'extended').items()
tweets = []
for tweet in trumptweets:
    tweets.append(tweet)
#Add twitter data into Tweets DataFrame

tweet_df = pd.DataFrame(data = [tweet.full_text for tweet in tweets], columns = ['Tweets'])
tweet_df['id'] = np.array([tweet.id for tweet in tweets])
tweet_df['date'] = np.array([tweet.created_at for tweet in tweets])
tweet_df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
tweet_df['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
tweet_df['source'] = np.array([tweet.source for tweet in tweets])

# Add Sentiment Polarity data into Tweets DataFrame
SA = []
for tweet in tweets:
    print(tweet.full_text)
    print(TextBlob(tweet.full_text).sentiment.polarity)
    if TextBlob(tweet.full_text).sentiment.polarity > 0:
        SA.append('Positive')
    elif TextBlob(tweet.full_text).sentiment.polarity == 0:
        SA.append('Neutual')
    else:
        SA.append('Negative')

tweet_df['SA'] = SA

#Add Hashtags data into Hashtags DataFrame
Hashtags = [[0],[1]]
for i in range(len(tweets)):
    for j in range(len(tweets[i].entities.get('hashtags'))):
        Hashtags[0].append(tweets[i].id)
        Hashtags[1].append(tweets[i].entities.get('hashtags')[j]['text'])
Hashtags_df = pd.DataFrame(data = np.array(Hashtags).T[1:, :], columns = ['tweet_id', 'Hashtags'])

#Add Mentions data into Mentions DataFrame
Mentions = [[0],[1], [2], [3]]
for i in range(len(tweets)):
    for j in range(len(tweets[i].entities.get('user_mentions'))):
        Mentions[0].append(tweets[i].id)
        Mentions[1].append(tweets[i].entities.get('user_mentions')[j]['id'])
        Mentions[2].append(tweets[i].entities.get('user_mentions')[j]['name'])
        Mentions[3].append(tweets[i].entities.get('user_mentions')[j]['screen_name'])
Mentions_df = pd.DataFrame(data = np.array(Mentions).T[1:, :], columns = ['tweet_id', 'User_id', 'name', 'screen_name'])
#---------------------
tweet_Pos = tweet_df[tweet_df.SA == 'Positive']
tweet_Neg = tweet_df[tweet_df.SA == 'Negative']
tweet_Neu = tweet_df[tweet_df.SA == 'Neutual']

writer = pd.ExcelWriter('TwitterData.xlsx', engine='xlsxwriter')
tweet_df.to_excel(writer, sheet_name = 'tweets')
Hashtags_df.to_excel(writer, sheet_name = 'hashtags')
Mentions_df.to_excel(writer, sheet_name = 'mentions')
