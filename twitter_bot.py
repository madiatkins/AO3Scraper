### Import modules
import itertools
import collections
import tweepy
import twitter_info 
import json
import sqlite3
import re

### Connect to tweepy and my Twitter account
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

### I need to convert the hannibal_fic_info.csv to JSON, and then open it
CACHE_FNAME = "hannibal_fic_info"

# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r', encoding="cp1252")
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

### Write info I want to database (I need to replay the info when I convert to JSON)

conn = sqlite3.connect("hannibal_fics.db")
cur = conn.cursor()


cur.execute("DROP TABLE IF EXISTS HannibalFics")
cur.execute("CREATE TABLE IF NOT EXISTS HannibalFics (tweet_ID INTEGER PRIMARY KEY, created_at TEXT, url TEXT, tweet_text TEXT, num_favorites INTEGER, num_retweets INTEGER, hashtags TEXT, media TEXT)")

for thing in CACHE_DICTION:
	cur.execute("INSERT INTO HannibalFics (tweet_ID, created_at, url, tweet_text, num_favorites, num_retweets, hashtags, media) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (x['id'], x['created_at'], x['source'], x['text'], x['favorite_count'], x['retweet_count'], str(x['entities']['hashtags']), str(x['entities'])))

conn.commit()


conn.close()





practice = [
	{"example tag haha": {
		"ship":"thorki", 
		"link":"https://archiveofourown.org"
	}},

	{"yet another example": {
		"ship":"stucky",
		"link":"https:archiveofourown.org/works"
	}}	
]	

### Following prints the pairing and link text I want in the reply, which takes from a list of dictionaries within dictionaries
for dict in practice:
    for dict2 in dict.values():
        x = f"pairing: {dict2['ship']}"
        y = f"link: {dict2['link']}"
        reply = x + '\n' + y
        print(reply)