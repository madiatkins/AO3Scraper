import json
import re
import sqlite3
import pprint
from pathlib import Path

# STEP 0: Enter the name of the JSON file you converted from the fic metadata (extract_metadata.py) CSV. Also, for testing, added PrettyPrint variable, if needed.
CACHE_FNAME = ""
pp = pprint.PrettyPrinter()

# STEP 1: Setting up cache to open file into an easy-to-use variable.
try:
    cache_file = open(CACHE_FNAME, 'r', encoding="cp1252")
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
    print("cache is open")
except:
    print("cache not open")


# STEP 2: Write the initial information I want into the database. I won't close the database until I've completed everything I need to do, but it is important to .commit() after you make changes. For sqlite.connect(), the file name is what you want the data to be called.
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
print("done with database!")


# Define functions needed to sort and clean the tags.

# Grab the word ID and tags for the fics from the database. Returns a list of tuples.
def grabfromdb():
    cur.execute("SELECT work_id, additional_tags FROM HannibalFics")
    grab_tags = cur.fetchall()
    print("pulled info from database")
    return grab_tags


# Create a dictionary from the list of tuples grabfromdb() returns to keep the word IDs associated with the tags.
def createdict_fromtuples(list_of_tuples):
    tuple_dict = {}
    for tup in list_of_tuples:
        key = tup[0]
        value = tup[1]
        tuple_dict[key] = value
    print("created tuple dictionary")
    return tuple_dict


# Use the two functions you just defined and assign the output to a variable.
tag_dict = createdict_fromtuples(grabfromdb())


# Create a separated list of tags for each key-value pair in the tag dictionary and reassigns that list of strings as the value. Separates based on ', '
def string_split(tagDict):
    for key, value in tagDict.items():
        splitup = re.split(', ', value)
        tagDict[key] = splitup
    print("strings are split")
    return tagDict


# Use the string_split() function on tag_dict and assign the output to a variable.
split = string_split(tag_dict)


# Dedupes a list of strings from the tag dictionary. Returns a tuple = (original tagDict, list of deduped tags)
def case_insensitive(tagDict):
    result = []
    marker = set()
    for key, value in tagDict.items():
        for tag in value:
            tag_lower = tag.lower()
            # test presence
            if tag_lower not in marker:
                marker.add(tag_lower)
                # preserve order
                result.append(tag)
    print("done deduping")
    return tagDict, result
    # returns tuple of dictionary, list


# Use the case_insensitive() function on split and assign the output to a variable.
deduped = case_insensitive(split)


# Writes the list of deduped tags to a .txt file for manual review.
# 'fname' is the string name for your file (remember to include .txt)
def write_list_to_file(deduped_tuple, fname):
    with open(fname, 'w') as file:
        big_list_o_tags = deduped_tuple[1]
        for tag in big_list_o_tags:
            file.write(tag + "\n")
    file.close()
    print("bad tags file is written")
    pass


# Checks if the manual review tag file exists. If it does, then it will not rerun write_list_to_file() function (which would undo any manual review you've done whenever you run this code). If it doesn't, then it will call the write_list_to_file() function which will write the tags to a file.
def does_file_exist(deduped_tuple, fname_full):
    path_to_file = fname_full
    path = Path(path_to_file)
    if path.is_file() is True:
        print("file already exists")
    if path.is_file() is False:
        print("file does not exist; writing file")
        write_list_to_file(deduped_tuple, path_to_file)
    pass


does_file_exist(deduped, "hannibal_ignoreList.txt")


# After the tags are written to the .txt file, you will need to manually go through and edit the file and remove any tags that shouldn't be ignored. It should *hopefully* not be as many since it was deduped.

# Creates a list of the manually updated tags from the file to which you wrote.
# 'fname' is the string name for your file (remember to include .txt)
def read_file_make_list(fname):
    with open(fname, 'r') as file:
        lines = file.read()
        bad_tags = lines.split('\n')
        return bad_tags


# Use the read_file_make_list() function and assign the output to a variable.
ignoreList = read_file_make_list("hannibal_ignoreList.txt")


# Creates a dictionary of unique tags assigned to their word ID from the tag dictionary created by string_split() compared against the ignoreList list of basic tags not to tweet.
def unique_tags(tagDict, notList):
    # reminder: key is an int and value is a list of strings
    for key, value in tagDict.items():
        unique_list = []
        for string in value:
            if string not in notList:
                unique_list.append(string)
            else:
                pass
        tagDict[key] = unique_list
    return tagDict


# Use the unique_tags() function and assign the output to a variable.
final_tag_dict = unique_tags(split, ignoreList)


# Use sqlite3 to update the existing database with the new list of updated tags to each row based on their work ID.
update_query = 'UPDATE HannibalFics SET additional_tags = ? WHERE work_id = ?'

sql_list = []
sql_list.append(final_tag_dict)

# sqlite3 is finicky so make sure to add str() and int() to the list of tags and work IDs respectively. Important to note that the additional_tags column is no longer a string of words, but a string of a list of strings.
for item1, item2 in sql_list[0].items():
    newtags = str(item2)
    ficid = int(item1)
    cur.execute(update_query, (newtags, ficid))
conn.commit()
print("updated database; closing database")
conn.close()
