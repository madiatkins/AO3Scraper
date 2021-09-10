### Import modules
import itertools
import collections
import tweepy
import twitter_info_hannibal 
import json
import sqlite3
import re

### Connect to tweepy and my Twitter account
consumer_key = twitter_info_hannibal.consumer_key
consumer_secret = twitter_info_hannibal.consumer_secret
access_token = twitter_info_hannibal.access_token
access_token_secret = twitter_info_hannibal.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

### I need to convert the hannibal_fic_info.csv to JSON, and then open it
CACHE_FNAME = "hannibal_fic_info2.json"

# Put the rest of your caching setup here:
try:
	cache_file = open(CACHE_FNAME,'r', encoding="cp1252")
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	print("cache not open")


### Write initial info I want to database
conn = sqlite3.connect("hannibal_fics.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS HannibalFics")
cur.execute("CREATE TABLE IF NOT EXISTS HannibalFics (work_id INTEGER PRIMARY KEY, title TEXT, relationship TEXT, additional_tags TEXT, link TEXT)")

for fic in CACHE_DICTION:
	cur.execute("INSERT INTO HannibalFics (work_id, title, relationship, additional_tags, link) VALUES (?, ?, ?, ?, ?)", (fic['work_id'], fic['title'], fic['relationship'], fic['additional tags'], 'https://archiveofourown.org/works/' + str(fic['work_id'])))

conn.commit()
conn.close()
print("done with database!")





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