import tweepy
from time import sleep
from secrets import *
hours = 60 * 60

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

f = open("./text.txt", "r")
lines = f.read().split("\n")
for line in lines: 
    if line != "":
        api.update_status(line) 
        sleep(1 * hours)
