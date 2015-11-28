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

    def search(self, query, count):
        return self.api.search(q=query, count=count)

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

if __name__ == "__main__":
    twitter = TwitterAPI()
    
    searched_tweets = []
    
    try:
        valid_tweet=None
        new_tweets = twitter.search(query="phyton", count=10)
        for tweet in new_tweets:

            valid, cause = isValid(tweet)
            if (valid):

                valid_tweet = tweet 
            else:
                print ("Text invalid:" +tweet.text)
                print ("Cause:" + cause)
        if (valid_tweet):
            print (tweet.text, tweet.id)
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        exit()
    