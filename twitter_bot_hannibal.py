# Import the libraries you will use throughout the code
import itertools
import collections
import tweepy
import twitter_info_hannibal
import json
import sqlite3
import re
import datetime

# Connect to tweepy and my Twitter account
# NEVER put your keys/secrets directly in your source code! Always import from a separate file

consumer_key = twitter_info_hannibal.consumer_key
consumer_secret = twitter_info_hannibal.consumer_secret
access_token = twitter_info_hannibal.access_token
access_token_secret = twitter_info_hannibal.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# You will need to convert the ao3_get_fanfics.py CSV output file to JSON to write to the sqlite3 database. I did this using (https://www.convertcsv.com/csv-to-json.htm), however, there are ways to do this in your code. Refer to (https://www.geeksforgeeks.org/convert-csv-to-json-using-python/) for steps

# Assign a variable to the JSON file you just converted
CACHE_FNAME = "hannibal_fic_info2.json"

# Open the file so it can be used in the rest of the code
try:
	cache_file = open(CACHE_FNAME, 'r', encoding="cp1252")
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	print("cache not open")


# Write the initial information I want in the database
# Connect to the sqlite3 by inputting a name for your database file
conn = sqlite3.connect("hannibal_fics.db")
cur = conn.cursor()

# Creates a table if one does not exist
cur.execute("DROP TABLE IF EXISTS HannibalFics")
cur.execute("CREATE TABLE IF NOT EXISTS HannibalFics (work_id INTEGER PRIMARY KEY, title TEXT, relationship TEXT, additional_tags TEXT, link TEXT)")

# For each dictionary in the list CACHE_DICTION, insert the relevant information into the database
for fic in CACHE_DICTION:
    cur.execute("INSERT INTO HannibalFics (work_id, title, relationship, additional_tags, link) VALUES (?, ?, ?, ?, ?)",
                (fic['work_id'], fic['title'], fic['relationship'], fic['additional tags'], 'https://archiveofourown.org/works/' + str(fic['work_id'])))
conn.commit()
# conn.close()
print("done with database!")


###########################
'''Have a function only run once (i.e., only run altar table once)

I would use a decorator on the function to handle keeping track of how many times it runs.

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def my_function(foo, bar):
    return foo+bar
Now my_function will only run once. Other calls to it will return None. Just add an else clause to the if if you want it to return something else. From your example, it doesn't need to return anything ever.

If you don't control the creation of the function, or the function needs to be used normally in other contexts, you can just apply the decorator manually as well.

action = run_once(my_function)
while 1:
    if predicate:
        action()
This will leave my_function available for other uses.

Finally, if you need to only run it once twice, then you can just do

action = run_once(my_function)
action() # run once the first time

action.has_run = False
action() # run once the second time


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

# Following prints the pairing and link text I want in the reply, which takes from a list of dictionaries within dictionaries
for dict in practice:
    for dict2 in dict.values():
        x = f"pairing: {dict2['ship']}"
        y = f"link: {dict2['link']}"
        reply = x + '\n' + y
        print(reply)
