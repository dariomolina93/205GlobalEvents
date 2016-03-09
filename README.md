Installation
-----------
1. - `cd tweepy` cd into the tweepy directory
2. - `py setup.py` install tweepy

Program Options
---------------
These can all be combined to refine your search

**follow**
A comma-separated list of user IDs, indicating the users whose Tweets should be delivered on the stream.
This will return:
- Tweets created by the user.
- Tweets which are retweeted by the user.
- Replies to any Tweet created by the user.
- Retweets of any Tweet created by the user.
- Manual replies, created without pressing a reply button (e.g. “@twitterapi I agree”).

The stream will not return:
- Tweets mentioning the user (e.g. “Hello @twitterapi!”).
- Manual Retweets created without pressing a Retweet button (e.g. “RT @twitterapi The API is great”).
- Tweets by protected users.

Example
`stream.filter(follow=USER_ID)` (Not tested yet, syntax may be wrong)

**track**
A comma-separated list of phrases which will be used to determine what Tweets will be delivered on the stream. You can think of commas as logical ORs, while spaces are equivalent to logical ANDs

Example
`stream.filter(track['trump'])`

**locations**
A comma-separated list of longitude,latitude pairs specifying a set of bounding boxes to filter Tweets by. Only geolocated Tweets falling within the requested bounding boxes will be included—unlike the Search API, the user’s location field is not used to filter tweets.

Example
`stream.filter(locations=-122.75,36.8,-121.75,37.8)` (Not tested yet, syntax may be wrong)

**Further details**
More details can be found on Twitter's `site
<https://dev.twitter.com/streaming/overview/request-parameters>`


Running the Program
-------------------
Run it from command line with the following command:
`py twitter_streaming.py TRACK_TERM`

It is currently set to run the stream while using the given TRACK_TERM. Certain keys have been selected to look for within the returned data structure. For best readability, pipe the results to a text file with a command similar to:
`py twitter_streaming.py trump > trump.txt`

Use CTRL+C to exit.

Current Issues
--------------
Attempting to print out emojis throws an error as there is no encoding for them the charmap of UTF-8
