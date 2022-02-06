# from pymongo import *
from asyncio import sleep
from datetime import *
import tweepy
from credentials import Config
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import pandas as pd

print("Initialized...")

ticker = ['$SQQQ', '$SPXS', '$SPXL', '$TQQQ', '$AMC', '$TSLA', '$GME', '$PYPL', '$AAPL', '$GOOGL']
words = ['buy', 'compra', 'long', 'short', 'sell', 'venta', 'vender']

print("Connected to twitter...")

auth = tweepy.OAuthHandler(Config.API_KEY, Config.API_SECRET_KEY)
auth.set_access_token(Config.ACCESS_TOKEN, Config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

matches = []


def get_twits() -> list:
    full_twit = []
    for emisora in ticker:
        print(f"Current Ticker: {emisora}")
        for twit in api.search_tweets(q=emisora, lang='es', tweet_mode='extended'):
            full_twit.append(f"{twit.user.name}, {twit.full_text}")
    return full_twit

extracted_twits  = get_twits()
pd_twits = pd.DataFrame({'Twit':extracted_twits})
pd_twits['matches'] = 0

for i in extracted_twits:
    matches.append(process.extractOne(
        i, words, scorer=fuzz.token_set_ratio))

pd_twits['matches'] = matches

print(pd_twits.head())