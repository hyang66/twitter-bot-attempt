import tweepy
from time import sleep
hours = 60 * 60
minutes = 60

from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth)

f = open("./text.txt", "r")
lines = f.read().split("\n")
for line in lines: 
    if line != "":
        print(line)
        api.update_status(line) 
        sleep(30* minutes)
