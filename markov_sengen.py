import random
from secrets import *

PUNCTUATION = {"\"", "-", ",", ".", "(", ")", "!", "?", " "}
NO_LEFT_SPACE = {"\"", "-", ",", ".", ")", "!", "?", " "}
NO_RIGHT_SPACE = {"\"", "-", "(", " "}

f = open("./corpus.txt", "r")
# we define sentences as a some text between new lines
lines = f.read().split("\n")

def process(s):
    """
    given a string, process it into a list such that:
    it is split on spaces, and punctuation
    """
    ans = []
    current_sampling = ""
    for i in range(len(s)):
        if s[i] in PUNCTUATION:
            if current_sampling != "":
                ans.append(current_sampling) 
                current_sampling = ""
            # also add in non-space punctuation
            if s[i] != " ":
                ans.append(s[i])
        else:
            current_sampling += s[i]
    if current_sampling:
        ans.append(current_sampling)
    return ans

def generate_links(lines, n):
    """
    generate dictionary of sequences of words that are linked
    using a frame of size n
    return list of words starting sentences and word frequencies
    """
    starting_words = []
    word_links = dict()
    for line in lines:
        line = process(line) 
        if len(line) > n:
            starting_words.append(tuple(line[i] for i in range(n)))
        
        for ind, word in enumerate(line):
            endpoint = min(ind + n, len(line))
            word_grouping = tuple(line[j] for j in range(ind, endpoint))
            # value of a word link is a list of words appearing immediately after
            # if the same word appears multiple times, it appears multiple times in
            # the list
            if word_grouping in word_links:
                if ind + n < len(line):
                    word_links[word_grouping].append(line[ind + n])
                else:
                    word_links[word_grouping].append("\n")
            else:
                word_links[word_grouping] = []
                if ind + n < len(line):
                    word_links[word_grouping].append(line[ind + n])
                else:
                    word_links[word_grouping].append("\n")
    return starting_words, word_links

starting_words, word_links = generate_links(lines, 1)

def generate_sentence(wl, sw):
    """
    Given a list of word links (wl) and starting words (sw),
    pick a random starting word link and generate sentences
    """
    rand = random.randrange(len(sw))
    gen_word = sw[rand]
    sentence = ""
    for word in gen_word[:-1]:
        sentence += word + " "
    # stop generating at the end of a line
    # corresponds to paragraph
    while not gen_word[-1] == "\n":
        new_word = gen_word[-1]
        # omit left space
        if new_word in NO_LEFT_SPACE:
            sentence = sentence[:-1]
        sentence += new_word + " "
        # omit right space
        if new_word in NO_RIGHT_SPACE:
            sentence = sentence[:-1]
        next_word_list = wl[gen_word]
        rand = random.randrange(len(next_word_list))
        # shift generated word over by one, and continue
        gen_word = (*(gen_word[1:]), next_word_list[rand])
    # strip out final space
    return sentence[:-1]


import tweepy
from os import environ
from time import sleep

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth)

# send a tweet!
while True:
    api.update_status(generate_sentence(word_links, starting_words))
    sleep(60*60)

def make_song():
    for i in range(4):
        for j in range(4):
            print(generate_sentence(word_links, starting_words))
        print("\n") 

# make_song()

