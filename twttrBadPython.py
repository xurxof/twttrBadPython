from  config import *
import tweepy, re
import os

last_id_filepath = os.path.join (os.path.dirname(os.path.realpath(__file__)),"lastid.txt")


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

    def sendDM (self, user_screen_name, text):
        return twitter.api.send_direct_message (user_screen_name, text=text)

def isValid (tweet):
    text = tweet.text.lower()
    if ('monty' in text) :
        return (False, 'monty  in text')
    if ('martens' in text) :
        return (False, 'martens in text') # a model of shoes :)
    
    p = re.compile(ur'\bphyton', re.IGNORECASE)
    if (not re.findall(p, text)):
        return (False, 'python not in text')
    return (True,'')

def readLastId ():
    try:
        file = open(last_id_filepath, "r")
        last_id = file.readline()
        return int(last_id)
    except:
        return -1

def saveLastId (id):
    file = open(last_id_filepath, "w")
    file.write(str(tweet.id))

def sendDirectMessage (twitter, tweet):
    if (not tweet or not DIRECT_MSG_USER):
        return
    url="https://twitter.com/" + tweet.user.screen_name + "/status/"+ str(tweet.id)
    directMsg = url + " - " + tweet.text
    twitter.sendDM(DIRECT_MSG_USER, text=directMsg)
    

if __name__ == "__main__":
    twitter = TwitterAPI()
    
    max_id= readLastId ()

    try:
        valid_tweet=None
        new_tweets = twitter.search(query="phyton", count=10, since_id= max_id+1)
        tweet=None
        for tweet in reversed(new_tweets):
            valid, cause = isValid(tweet)
            if (valid):

                valid_tweet = tweet 
                break
            else:
                print (cause, tweet.text)
        if (valid_tweet):
            saveLastId(valid_tweet.id)
            print ('selected tweet: ', tweet.text)
            sendDirectMessage (twitter, valid_tweet)
        elif (tweet):
            saveLastId(tweet.id)
    except tweepy.TweepError as e:
        print (e)
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        exit()
    