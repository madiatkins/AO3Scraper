# STEP 0: Import the libraries you will use throughout the code
import itertools
import collections
import tweepy
import twitter_info_hannibal
import json
import sqlite3
import re
import datetime

### IMPORTANT ###
# You *MUST* run:
# 1) ao3_work_ids.py to gather fic work IDs,

# 2) ao3_get_fanfics.py to gather the fic data from the work IDs,

# 3) extract_metadata.py to generate a CSV of only the metadata (i.e., no fanfic chapters since you don't need them),

# 4) manually convert the metadata CSV to a JSON file (there is code for this, but it's easier for me using [https://www.convertcsv.com/csv-to-json.htm] - if you'd like to do it via code refer to [https://www.geeksforgeeks.org/convert-csv-to-json-using-python/] for steps), and

# 5) generate_tags_list.py on the metadata JSON file to create a database and a list of tags to tweet BEFORE using this bot. There is no caching or cleaning of fic data in this code.


# STEP 1: Connect to tweepy and your Twitter account (i.e., the tag account)
# REMEMBER to NEVER put your keys/secrets directly in your source code! Always import from a separate file and do not push that file to GitHub.

consumer_key = twitter_info_hannibal.consumer_key
consumer_secret = twitter_info_hannibal.consumer_secret
access_token = twitter_info_hannibal.access_token
access_token_secret = twitter_info_hannibal.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# STEP 2: Open the file containing the final tags list.

def read_file_extract_list(fname):
	#'fname' is a file name with .txt at the end.
	with open('fname', 'r') as file:
		lines = file.read()
		final_tags = lines.split('\n')
		return final_tags




# Following prints the pairing and link text I want in the reply, which takes from a list of dictionaries within dictionaries
for dict in practice:
    for dict2 in dict.values():
        x = f"pairing: {dict2['ship']}"
        y = f"link: {dict2['link']}"
        reply = x + '\n' + y
        print(reply)
