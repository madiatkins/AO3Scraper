import itertools
import collections
import json
import re
import sqlite3
import tweepy
import twitter_info_hannibal
import datetime

CACHE_FNAME = "hannibal_fic_info2.json"

# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME, 'r', encoding="cp1252")
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
	print("cache not open")

# Write the initial information I want in the database. I won't close the database until I've completed everything I need to do
conn = sqlite3.connect("hannibal_fics.db")
cur = conn.cursor()

# Creates a table if one does not exist
cur.execute("DROP TABLE IF EXISTS HannibalFics")
cur.execute("CREATE TABLE IF NOT EXISTS HannibalFics (work_id INTEGER PRIMARY KEY, title TEXT, relationship TEXT, additional_tags TEXT, link TEXT)")

# For each dictionary in the list CACHE_DICTION, insert the relevant information into the database
for fic in CACHE_DICTION:
	cur.execute("INSERT INTO HannibalFics (work_id, title, relationship, additional_tags, link) VALUES (?, ?, ?, ?, ?)", (fic['work_id'], fic['title'], fic['relationship'], fic['additional tags'], 'https://archiveofourown.org/works/' + str(fic['work_id'])))
conn.commit()
# conn.close()
print("done with database!")

# Define functions needed to sort and clean the tags


def grabfromdict():
	empty_str = ""
	cur.execute("SELECT work_id, additional_tags FROM HannibalFics WHERE additional_tags != empty_str")
	grab_tags = cur.fetchall()
	print("pulled info from database")
	return grab_tags


# takes string and splits it into a list of separated strings based on ', '
def string_split(tag_string):
	splitup = re.split(', ', tag_string)
	return splitup


# takes list of strings and dedupes it
def case_insensitive(tag_list):
	result = []
	marker = set()

	for sensitive_tag in tag_list:
		tag_lower = sensitive_tag.lower()
		# test presence
		if tag_lower not in marker:
			marker.add(tag_lower)
			# preserve order
			result.append(sensitive_tag)
	print("done deduping")
	return result


def grabfromdict():
	empty_str = ""
	cur.execute("SELECT work_id, additional_tags FROM HannibalFics WHERE additional_tags != empty_str")
	grab_tags = cur.fetchall()
	print("pulled info from database")
	return grab_tags


def write_list_to_file(big_list_o_tags):
	with open('manual_look_tags.txt', 'w') as file:
		for tag in big_list_o_tags:
			file.write(tag + "\n")
	file.close()
	print("bad tags file is written")
	pass


def read_file_make_list():
	with open('manual_look_tags.txt', 'r') as file:
		lines = file.read()
		bad_tags = lines.split('\n')
		return bad_tags


# takes two lists: list of tags from row and pre-defined notList
def unique_tags(myList, notList):
	unique_list = []
	for x in myList:
		if x not in notList:
			unique_list.append(x)
		else:
			pass
	return unique_list
		
