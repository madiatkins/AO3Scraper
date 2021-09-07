# Mads edition!
This repository is made with the help of the wonder AO3Scraper repository. I am making a Twitter bot that will post Archive of Our Own fanfiction tags for certain fandoms on respective Twitter accounts. The twitter_bot.py file will include the code required to make the bot work.

The process goes as follows:
1. Use the AO3Scraper code to pull data from Archive of Our Own. From this data, I will separate out the tags it gathers and manually go through to clean up duplicates and non-relevant tags. (We want our tags to be funny and custom!)
2. Place the data in a database using SQLite3 for easy reference and pulling of information as needed.
3. Create a dictionary where the key is the tag and the value is a custom string "template" of the fanfiction information (ship/paring and link to the fic itself) which I will gather from the database. This will be used later to create a reply to the original tweet.
4. Using the Twitter API's POST status call, I will grab from the database to tweet tags to a specific account. I will gather the response in a JSON file.
5. Update the database to include the tweet ID of the tag just posted.
6. Grab from the database the tweet ID in order to use the Twitter API's POST status call again, but use in_reply_to_status_id to reply to the tweet that will include the fanfiction information (ship/pairing and link to the fic itself).
7. The response from in_reply_to_status_id will be placed in a JSON for archival purposes. I do not have plans to use that data right now, but good to have.

Please note that it has been years since I last coded in Python, and I have never pushed information to Twitter using their API - I have only ever pulled information from Twitter. Because of htis, my code will not be super clean or perfect in any way, but I hope that it will get the job done.

Anyone and everything is allowed to use this code to develop their own AO3 Twitter tag bots or fork and expand upon it for your own ideas. I'd love to hear about your ideas and customization of the code if you do so! Feel free to email me at madqueeen.ao3@gmail.com!

Below you will find the original README text from the AO3Scraper repository - HUGE shoutout to them for developing an awesome tool like this!! :D



# AO3Scraper

In collaboration with [@ssterman](https://github.com/ssterman). A simple Python [Archive of Our Own](https://archiveofourown.org/) scraper. Now with HASTAC 2017 [presentation slides](https://docs.google.com/presentation/d/1GrpMYw25Bz_m0r2hv0Orgp-uxSIi4HdrHpzL6deCopc)!

Features:
- Given a fandom URL and amount of fic you want, returns a list of the fic IDs. (ao3_work_ids.py)
- Given a (list of) fic ID(s), saves a CSV of all the fic metadata and content. (ao3_get_fanfics.py)
- Given the CSV of fic metadata and content created by ao3_get_fanfics.py, saves a new CSV of only the metadata. (extract_metadata.py)
- Given the CSV of fic metadata and content created by ao3_get_fanfics.py, creates a folder of individual text files containing the body of each fic (csv_to_txts.py)
- Given the CSV of fic metadata and content created by ao3_get_fanfics.py, uses an AO3 tag URL to count the number of works using that tag or its wrangled synonyms (get_tag_counts.py)
- (new!) Scrape users who have authored, kudos-ed, bookmarked (``get_authors, get_kudos, get_bookmarks`` functions)
- (new!) Scrape fics of only a certain language

## Dependencies
- pip install bs4
- pip install requests
- pip install unidecode

## Example Usage

Let's say you wanted to collect data from the first 100 English completed fics, ordered by kudos, in the Sherlock (TV) fandom. The first thing to do is use AO3's nice search feature on their website.

We get this URL as a result: http://archiveofourown.org/works?utf8=%E2%9C%93&work_search%5Bsort_column%5D=kudos_count&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=1&work_search%5Bcomplete%5D=0&work_search%5Bcomplete%5D=1&commit=Sort+and+Filter&tag_id=Sherlock+%28TV%29 

Run `python ao3_work_ids.py <url>`. You can optionally add some flags: 
- `--out_csv output.csv` (the name of the output csv file, default work_ids.csv)
- `--num_to_retrieve 10` (how many work ids you want, defaults to all)
- `--multichapter_only 1` (restricts output to only works with more than one chapter, defaults to false)
- `--tag_csv name_of_csv.csv` (provide an optional list of tags; the retrieved fics must have one or more such tags. default ignores this functionality)

The only required input is the search URL.  

For our example, we might say: 

`python ao3_work_ids.py "http://archiveofourown.org/works?utf8=%E2%9C%93&work_search%5Bsort_column%5D=kudos_count&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=1&work_search%5Bcomplete%5D=0&work_search%5Bcomplete%5D=1&commit=Sort+and+Filter&tag_id=Sherlock+%28TV%29" --num_to_retrieve 100 --out_csv sherlock`

Now, to actually get the fics, run `python ao3_get_fanfics.py sherlock.csv`. You can optionally add some flags: 
- `--csv output.csv` (the name of the output csv file, default fanfic.csv)
- `--header 'Chrome/52 (Macintosh; Intel Mac OS X 10_10_5); Jingyi Li/UC Berkeley/email@address.com'` (an optional http header for ethical scraping)
- `--lang English` (scrapes fics of only a specific language, this argument will not work if you use incorrect spelling and/or capitalization, if this argument is not used the program will scrape all fics regadless of language) Note: if the desired language is not English, then you will have to input the name of that language as it appears on AO3, for example if you want your fics to be in French the argument after `--lang` should be 'Francais' not 'French', including any accents in the input language will also not work.
- `--bookmarks` includes the users who have bookmarked a fic.  For fics with many bookmarks, this is a slow operation. 

If you don't want to give it a .csv file name, you can also query a single fic id, `python ao3_get_fanfics.py 5937274`, or enter an arbitrarily sized list of them, `python ao3_get_fanfics.py 5937274 7170752`.

If you stop a scrape from a csv partway through (or it crashes), you can restart from the last uncollected work_id using the flag `--restart 012345` (the work_id).  The scraper will skip all ids up to that point in the csv, then begin again from the given id. 

By default, we save all chapters of multi-chapter fics. Use `--firstchap 1` to only retrieve the first chapter of multichapter fics. 

We cannot scrape fics that are locked (for registered users only), but submit a pull request if you want to build authentication! 

**Note that the 5 second delays before requesting from AO3's server are in compliance with the AO3 terms of service.  Please do not remove these delays.**

Happy scraping! 

## Improvements

We love pull requests!

## FF.net

Want to scrape fanfiction.net? Check out my friend [@smilli](https://github.com/smilli/)'s [ff.net scraper](https://github.com/smilli/fanfiction)! 

## License
This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Feel free to use it and adapt it however you want, but don't make money off of it!
