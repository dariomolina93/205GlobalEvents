
# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from string import punctuation

# Import other necessary libraries
from threading import Thread
import sys
import json
import time
import urllib.request

# Import libraries for plotting on graphs
import plotly.plotly as py
import plotly.graph_objs as go

# Twitter API access keys. There are two sets so that we can access twice as many without getting Rate Limiting Errors
consumer_key = ["4mSPfcXaSASQiR1FIZ5ccc0tB", "YS0KGexQmvlJhGqHUfrNey7ks"]
consumer_secret = ["U8VzCgpKjFwf0qUCik4s3VefQCjZY6g0g6mHOKw7CMeVTHw7xy", "VXVFCGQrzc8syovgscnU8U6C7mYU0886HTz2JGSSlJnI8l57Ru"]
access_token = ["3236861032-tJTYWFajn9m5Us1kfvW0hAZawQEPhzLHdTZXB6z", "707646836094345216-n6u7xEFTTPkJdIkzI7vrBfLRSAIpEh9"]
access_token_secret = ["uUTkpeIHNC5JWfznu0BgkdwGABv55hXIBylTEB5iOm7iv", "6kJsB9ToFcwfWuvY0r01xYyLvQHI3gg1B6AKLhUDVSkIY"]

# Search keys for the return objects for Twitter and Instagram (i..) APIs
keys = ['created_at', 'id', 'timestamp_ms', 'source', 'in_reply_to_status_id', 'text']
userKeys = ['id', 'time_zone', 'name', 'screen_name', 'followers_count', 'friends_count', 'listed_count', 'favourites_count', 'statuses_count', 'created_at', 'lang', 'profile_image_url']
iDataKeys = ['type', 'caption', 'link', 'created_time', 'id']
iLocationKeys = ['name', 'id', 'latitude', 'longitude']
iUserKeys = ['username', 'full_name', 'profile_picture', 'id']

#Opening files that contains the positive and negative words to do our sentiment analysis
pos_sent = open("POSITIVE.txt").read()
positive_words=pos_sent.split('\n')

neg_sent = open('NEGATIVE.txt').read()
negative_words=neg_sent.split('\n')

# Structure for holding our objects
totalTweets = []
totalInstagrams = []
threads = []
stdOuts = []
countriesInstagrams = {}
twitterCountryList = {}
# This is how long we will run our program for in seconds
RUN_TIME = 60

# Interval to tell user that time has passed
INTERVAL_DURATION = 5

# Counters for total sentiment words in Sentiment Analysis
totalPositiveTweets = 0
totalNegativeTweets = 0
totalNeutralTweets= 0
totalTweets = 0

totalPositiveInsta = 0
totalNegativeInsta = 0
totalNeutralInsta = 0
totalInsta = 0

validLetters = "abcdefghijklmnopqrstuvwxyz "#list that contains the only chars acceptable in tweet and insta post

def getToneTwitter(text): 
        tweets_list = text.split('\n')#split the tweet into single words
        tweetListSize = len(tweets_list)#length of tweet
        # print("TweetListSize: ",tweetListSize)# print the length of tweet to screen

        newString = " "#string to place in our tweet that will be filtered

        for tweets in tweets_list:#for loop that goes through each words in the loop
           positive_counter=0#for each incoming tweet have a positive and negative counter that keeps track of the positive or negative words in the tweet
           negative_counter=0
            
           tweet_processed=tweets.lower()#make all the letters in tweet lowercase


           for char in tweet_processed:#goes through each char in the tweet
              if char in validLetters:#if char is in the list of letters that are acceptable, add them and concatenate them to newString
                newString += char#newString will now contain our tweet that has been parsed through


           # words = newString.split(' ')# split the tweet into a list and seprate them by spaces

           for p in list(punctuation):
             newString = newString.replace(p, ' ')
             words = newString.split(' ')

           index = 0# index of list

           for wor in words:# go through each of the words in the list
             if wor == '':#if it finds and empty string or space for any element in our list, deleted it at that index
               del words[index]
             index = index + 1#increment our index after before every iteration

           index2 = 0#we needed to add this counter and for loop as a double filter for we had problems where some unary code symbols would be send to our negative counter
           for wor in words:
              if(wor == '' or wor == ' '):
                 del words[index2]
              index2 = index2 + 1

           for word in words:#go through each words and check to see if that word is in positive list or negative list

                 if word in negative_words:#if its found display the word and increase their respective counter
                    # print("NEGATIVE WORD: ", word)
                    negative_counter=negative_counter+1

                 elif word in positive_words:
                    # print("POSITIVE WORD: ", word)
                    positive_counter=positive_counter+1#if it finds the word on either list, increment that counter and print the word

        global totalPositiveTweets# we need to make these global so we dont have any erros
        global totalNegativeTweets
        global totalNeutralTweets
        global totalTweets

        #This is where we check to see if the tweet is positive, negative or neutral
        if(positive_counter > negative_counter):#if the amount of positive words found in the tweet were higher than the amount of negative words,  then tweet is positive
           # print("This post is Positive!")
           totalPositiveTweets = totalPositiveTweets + 1#add to total positive tweets for this search

        elif(positive_counter < negative_counter):#if the amount of negative words were higher than positive, than tweet is negative and increment counter like previous if statement
           # print("This post is Negative!")
           totalNegativeTweets = totalNegativeTweets + 1

        else:#if the amount of postivie words were equal to negative words, than tweet is netural; increment counter
           # print("This post is Neutral")
           totalNeutralTweets = totalNeutralTweets + 1

        print("Total Positive Tweets: ") #display the total positive tweets for 
        print(totalPositiveTweets)

        print("Total Negative Tweets: ")
        print(totalNegativeTweets)

        print("Total Neutral Tweets: ")
        print(totalNeutralTweets)

        totalTweets = totalTweets + 1#keeps track of how many incoming tweets there are for the current search
        print ("Total Number of Tweets: ")
        print (totalTweets)
        print("\n\n")
#********************************************************************************************

def getToneInstagram(text): #It was followed by tweeter but pretty much everywhere that says tweeter is going to represent instagram within this scope

        tweets_list = text.split('\n')#split the tweet into single words
        tweetListSize = len(tweets_list)#length of tweet
        # print("TweetListSize: ",tweetListSize)# print the length of tweet to screen

        newString = " "#string to place in our tweet that will be filtered

        for tweets in tweets_list:#for loop that goes through each words in the loop
           positive_counter=0#for each incoming tweet have a positive and negative counter that keeps track of the positive or negative words in the tweet
           negative_counter=0
            
           tweet_processed=tweets.lower()#make all the letters in tweet lowercase


           for char in tweet_processed:#goes through each char in the tweet
              if char in validLetters:#if char is in the list of letters that are acceptable, add them and concatenate them to newString
                newString += char#newString will now contain our tweet that has been parsed through


           # words = newString.split(' ')# split the tweet into a list and seprate them by spaces

           for p in list(punctuation):
             newString = newString.replace(p, ' ')
             words = newString.split(' ')

           index = 0# index of list

           for wor in words:# go through each of the words in the list
             if wor == '':#if it finds and empty string or space for any element in our list, deleted it at that index
               del words[index]
             index = index + 1#increment our index after before every iteration

           index2 = 0
           for wor in words:
              if(wor == '' or wor == ' '):
                 del words[index2]
              index2 = index2 + 1

           for word in words:#go through each words and check to see if that word is in positive list or negative list

                 if word in negative_words:#if its found display the word and increase their respective counter
                    # print("NEGATIVE WORD: ", word)
                    negative_counter=negative_counter+1

                 elif word in positive_words:
                    # print("POSITIVE WORD: ", word)
                    positive_counter=positive_counter+1#if it finds the word on either list, increment that counter and print the word

        global totalPositiveInsta# we need to make these global so we dont have any erros
        global totalNegativeInsta
        global totalNeutralInsta
        global totalInsta

        #This is where we check to see if the tweet is positive, negative or neutral
        if(positive_counter > negative_counter):#if the amount of positive words found in the tweet were higher than the amount of negative words,  then tweet is positive
           # print("This post is Positive!")
           totalPositiveInsta = totalPositiveInsta + 1#add to total positive tweets for this search

        elif(positive_counter < negative_counter):#if the amount of negative words were higher than positive, than tweet is negative and increment counter like previous if statement
           # print("This post is Negative!")
           totalNegativeInsta = totalNegativeInsta + 1

        else:#if the amount of postivie words were equal to negative words, than tweet is netural; increment counter
           # print("This post is Neutral")
           totalNeutralInsta = totalNeutralInsta + 1

        print("Total positive Instagram posts: ") #display the total positive tweets for 
        print(totalPositiveInsta)

        print("Total negative Instagram posts: ")
        print(totalNegativeInsta)

        print("Total Neutral Instagram posts: ")
        print(totalNeutralInsta)

        totalInsta = totalInsta + 1#keeps track of how many incoming tweets there are for the current search
        print ("Total Number of Instagram Posts: ")
        print (totalInsta)
        print("\n\n")
# Catch the StdOut for the Stream, and redirect the data so that we can mine it
#**********************************************************************************************
print("Before STDOUTLISTENER!!")
class StdOutListener(StreamListener):

    # When we receive data
    def on_data(self, data):
        # Get our global list of our tweets and the startTime
        global totalTweets
        global startTime

        # Dictionaries for mining and re-storing the data we find.
        dataStruct = {}
        userData = {}

        # Run this thread until our RUN_TIME has been reached
        if startTime + RUN_TIME < time.time():
            sys.exit(0)

        # Very hacky solution for determining which std out listener is for which search term
        # If this listener is not in our list of listeners, then we create a new list,
        # append it to the global totalTweets list, and add the listener to the list of listeners.
        # Basically, check to see if this is the first time running this listener. If it is,
        # then add it so we can check to see if it comes up again
        if self not in stdOuts:
            tweets = []
            stdOuts.append(self)
            totalTweets.append(tweets)

        # Get the JSON data from our listener
        jsonData = json.loads(data)

        # Iterate through the keys to create our object, and append it to our global list
        try:
            for key in keys:
                dataStruct[key] = jsonData[key]
            for userKey in userKeys:
                userData[userKey] = jsonData['user'][userKey]
            dataStruct['user'] = userData
            totalTweets[stdOuts.index(self)].append(dataStruct) # stdOuts.index(self) means we get the number of this listener, which will correspond to the search term
        
            tweet = jsonData['text']
            print("BEFORE TWITTER SENTIMENT ANALYSIS!")
            getToneTwitter(tweet)#Sentiment analysis on our incoming tweet

            if jsonData['coordinates'] == None:
              print ("There were no coordinates for this tweet\n")

            else: 
              print ("COORDINATES OF THE TWEET!!!!!!!!!!!!!!!!!!!!")
              print (jsonData['coordinates'])
              latitude = jsonData["coordinates"]["coordinates"][0]
              longitude = jsonData["coordinates"]["coordinates"][1]
              #print"LATITUDE: ", latitude
              #print "LONGITUDE: ", longitude
              country = getplace(latitude, longitude)

              if country in twitterCountryList:
               twitterCountryList[country] += 1

              else:
               twitterCountryList[country] = 1

              print ("Tweet Countries: ")
              print(twitterCountryList)

        except KeyError:
            pass # created_at not present for some reason

    # If the listener encounters an error of some sort
    def on_error(self, status):
        if status == 420:
            print("Rate Limiting Error")
        else:
            print(status)

# Function for getting the country name from the coordinates
def getPlace(lat, lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" % (lat, lon)
    response = urllib.request.urlopen(url)
    v = response.read()
    j = json.loads(v.decode("utf-8"))
    country = None
    
    if j['results']:
        components = j['results'][0]['address_components']
        
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
    return country

# Function for getting the tweets (in conjunction with StdOutListener)
def getTweets(trackString, index):
    # This is simply to choose between API keys. Even numbered search terms
    # get keys at [0], odds get keys at [1]
    index = index%2

    # This handles Twitter authetication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key[index], consumer_secret[index])
    auth.set_access_token(access_token[index], access_token_secret[index])
    stream = Stream(auth, l)

    # This line filters Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[trackString])

# Function for getting the instas
def getInstaPosts(searchTag):
    # Use our global variables so we can access them later/they are uniform everywhere
    global totalInstagrams
    global startTime
    # List for collecting instas for a particular tag
    instagrams = []

    # Add that list to the global one
    totalInstagrams.append(instagrams)

    # This will be our first URL that we will hit for getting our instagram data, adding in the search term
    next_url = "https://api.instagram.com/v1/tags/" + searchTag + "/media/recent?access_token=145161542.1fb234f.afe13baad0e2403ea0a650b7aeacfe6b"

    # Run this until our RUN_TIME has been reached
    while startTime + RUN_TIME > time.time():
        # Get the data and retrieve the next URL. This will point us to older posts
        # fitting the same tags, as opposed to twitter which gives us current ones.
        # May encounter HTTP Error 429, which is too many requests
        jsonData = json.loads(urllib.request.urlopen(next_url).read().decode('utf-8'))
        next_url = jsonData['pagination']['next_url']

        # For each insta we get, create necessary structures, and fill them out with the appropriate data
        for index in range(0, len(jsonData)):
            instaData = {}
            location = {}
            tags = []
            comments = {}
            userData = {}

            for key in iDataKeys:
                instaData[key] = jsonData['data'][index][key]
            if jsonData['data'][index]['location']:
                for key in iLocationKeys:
                    location[key] = jsonData['data'][index]['location'][key]
                if jsonData['data'][index]['location']:
                    instaData['location'] = location
                    # increment the country in the list
                    country = getPlace(location['latitude'], location['longitude'])
                    if country in countriesInstagrams:
                        countriesInstagrams[country] += 1
                    else:
                        countriesInstagrams[country] = 1
                    # print countries list                
                    # print(str(countriesInstagrams))

            for tag in (jsonData['data'][index]['tags']):
                tags.append(tag)
            instaData['tags'] = tags
            instaData['like_count'] = jsonData['data'][index]['likes']['count']
            instaData['comment_count'] = jsonData['data'][index]['comments']['count']
            for user in jsonData['data'][index]['comments']['data']:
                comments[user['from']['username']] = user['text']
            instaData['comments'] = comments
            for key in iUserKeys:
                userData[key] = jsonData['data'][index]['user'][key]
            instaData['user'] = userData
            instaData['media_url'] = jsonData['data'][index][instaData['type'] + "s"]['standard_resolution']['url']
            
            instagrams.append(instaData)  

            # get the tone of the caption and hashtags
            text = ""
            if instaData['caption']['text'] :
                # print(str(instaData['caption']['text']))
                text = instaData['caption']['text']
 
        getToneInstagram(text)#Sentiment analysis for instagram posts
        # print countries list                
        print(str(countriesInstagrams))

startTime = time.time()
nextInterval = INTERVAL_DURATION

# Delete the first sys.argv, which is the file name (events.py). Simply
# makes it easier to iterate.
del(sys.argv[0])

# For each term, create new twitter and instagram threads to get the appropriate data
for term in sys.argv:
    newInstaThread = Thread(target=getInstaPosts, args=(term,))
    newTwitterThread = Thread(target=getTweets, args=(term,sys.argv.index(term)))
    newInstaThread.daemon = True
    newTwitterThread.daemon = True
    newInstaThread.start()
    newTwitterThread.start()

    threads.append(newInstaThread)
    threads.append(newTwitterThread)

# Iterate until all threads have ended (all have run for RUN_TIME)
while len(threads) > 0:
    if startTime + nextInterval < time.time():
        print("Process has been running for " + str(nextInterval) + " of " + str(RUN_TIME) + " seconds...")
        nextInterval += INTERVAL_DURATION
    for thread in threads:
        if not thread.isAlive():
            del(threads[threads.index(thread)])

# Store data for our graphs
tweetsPerMinute = []
instagramsPerMinute = []

# For each term, iterate through their respective lists and print out some stats
for arg in sys.argv:
    index = sys.argv.index(arg)

    tweetCount = len(totalTweets[index])
    instaCount = len(totalInstagrams[index])
    newestPostTime = int(totalInstagrams[index][0]['created_time'])
    oldestPostTime = int(totalInstagrams[index][len(totalInstagrams[index]) - 1]['created_time'])

    tweetsPerMinute.append(tweetCount*60/RUN_TIME)
    instagramsPerMinute.append(instaCount*60/((newestPostTime - oldestPostTime)/1000))

# Create data structures for our graphing library
twitter = go.Bar(
    x=sys.argv,
    y=tweetsPerMinute,
    name='Twitter'
)

instagram = go.Bar(
    x=sys.argv,
    y=instagramsPerMinute,
    name='Instagram'
)

data = [twitter, instagram]
layout = go.Layout(
    barmode='stack',
    title='Social Media Mentions',
    yaxis= dict(
        title='Mentions (per minute)',
    ),
)

# Create graphs to visualize our data
fig = go.Figure(data=data, layout=layout)
plot_url = py.plot(fig, filename='stacked-bar')
#events.pyOpen
#Displaying events.py.

