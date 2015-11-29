from  config import *
import tweepy

class TwitterAPI:
    def __init__(self):
        consumer_key = APP_KEY
        consumer_secret = APP_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = OAUTH_TOKEN
        access_token_secret = OAUTH_TOKEN_SECRET
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)

    def search(self, query, count, since_id):
        return self.api.search(q=query, count=count, since_id=since_id, lang="es")

def isValid (tweet):
    text = tweet.text.lower()
    if ('phyton' not in text) :
        return (False, 'python not in text')
    if ('monty' in text) :
        return (False, 'monty  in text')
    if ('martens' in text) :
        return (False, 'martens in text') # a model of shoes :)
    if (tweet.id in [670651635048316928]) :
        return (False, 'reponsed in text')
    return (True,'')

def readLastId ():
    try:
        file = open("lastid.txt", "r")
        last_id = file.readline()
        return int(last_id)
    except:
        return -1

def saveLastId (id):
    file = open("lastid.txt", "w")
    file.write(str(tweet.id))


if __name__ == "__main__":
    twitter = TwitterAPI()
    
    max_id= readLastId ()

    try:
        valid_tweet=None
        new_tweets = twitter.search(query="phyton", count=10, since_id= max_id+1)
        for tweet in reversed(new_tweets):

            valid, cause = isValid(tweet)
            if (valid):
                # print (tweet)
                valid_tweet = tweet 
                break
        if (valid_tweet):
            statusUrl = "https://twitter.com/" + tweet.user.screen_name + "/status/"+ str(tweet.id) + " - " + tweet.text
            # print ("Selected: ", tweet.text, tweet.id,tweet.user.screen_name)
                
            saveLastId(tweet.id)
            dirMsg = twitter.api.send_direct_message ("xurxof",statusUrl)
            print(statusUrl,dirMsg)
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        exit()
    