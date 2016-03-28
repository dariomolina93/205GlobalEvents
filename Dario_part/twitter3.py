from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
import json
import time

ckey = "YS0KGexQmvlJhGqHUfrNey7ks"
csecret = "VXVFCGQrzc8syovgscnU8U6C7mYU0886HTz2JGSSlJnI8l57Ru"
atoken = "707646836094345216-n6u7xEFTTPkJdIkzI7vrBfLRSAIpEh9"
asecret = "6kJsB9ToFcwfWuvY0r01xYyLvQHI3gg1B6AKLhUDVSkIY"

word = raw_input("Hello, what would you like to search for?")# ask user input 



class StdOutListener(StreamListener):

    def on_data(self, data):# bringing in the data
        try:# codition to check if all of this works
            incomingData = json.loads(data)# all the data incoming we are going to load it into a json file
            tweet = incomingData["text"]# from the incoming data store text in tweet: we dont use user in front of it for json is formatted into dictionaries for each object. So text, created_at, and user are own object and inside the object it has dictionaries that for each key theres a specific value for example {user : name}
            username = incomingData["user"]["name"]
            screenName = incomingData["user"]["screen_name"]# we are storing each 
            description = incomingData["user"]["description"]
            created = incomingData["created_at"]
            profile_img = incomingData["user"]["profile_image_url"]
            location = incomingData["user"]["location"]
            follower = incomingData["user"]["followers_count"]
            friends = incomingData["user"]["friends_count"]
            listed = incomingData["user"]["listed_count"]
            #media = all_data["entities"]["media"][0]["media_url_https"]

            #tweet=tweet.encode("utf-8")
            #tweet=tweet.decode("utf-8")
            print 'User: ', ((username))
            print 'Screen Name: ', ((screenName))
            print 'Description: ', ((description))
            print 'Date: ', ((created))
            print 'Location: ', ((location))
            print 'Tweet: ', ((tweet))
           # print 'Shared Media: ', ((media))
            print 'Profil Image URL: ', ((profile_img))
            print 'Follower: ', ((follower))
            print 'Friends: ', ((friends))
            print 'Listed: ', ((listed))
            print '\n\n'

            saveFile = open('tweets.json','a')
            saveFile.write(data)
            saveFile.write('\n')
            saveFile.close()
            
            return True
            
        except Exception as e:
            print 'failed on data,',str(e)
            time.sleep(5)



    def on_error(self, status):
        print status

l = StdOutListener()
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

stream = Stream(auth, l)
stream.filter(track = word)
