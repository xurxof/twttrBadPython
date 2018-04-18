# -*- coding: utf-8 -*-
from config import *
import tweepy, re
import os

last_id_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lastid.txt")


class TwitterAPI:
    def __init__(self):
        consumer_key = APP_KEY
        consumer_secret = APP_SECRET
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = OAUTH_TOKEN
        access_token_secret = OAUTH_TOKEN_SECRET
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message, in_reply_to_status_id):
        self.api.update_status(status=message, in_reply_to_status_id=in_reply_to_status_id)

    def search(self, query, count, since_id):
        return self.api.search(q=query, count=count, since_id=since_id, lang="es")

    def send_direct_msg(self, user_screen_name, text):
        return twitter.api.send_direct_message(user_screen_name, text=text)


def is_valid(tweet):
    text = tweet.text.lower()
    if 'monty' in text:
        return False, 'monty  in text'
    if 'monthy' in text:
        return False, 'monthy  in text'
    if 'martens' in text:
        return False, 'martens in text'  # a model of shoes :)

    p = re.compile(r'\bphyton', re.IGNORECASE)
    if not re.findall(p, text):
        return False, 'phyton not in text'
    return True, ''


def read_last_id():
    try:
        file = open(last_id_filepath, "r")
        last_id = file.readline()
        return int(last_id)
    except:
        return -1


def save_last_id(id):
    file = open(last_id_filepath, "w")
    file.write(str(tweet.id))


def send_direct_message(twitter, tweet):
    if not tweet or not DIRECT_MSG_USER:
        return
    url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
    directmsg = url + " - " + tweet.text
    twitter.send_direct_msg(DIRECT_MSG_USER, text=directmsg)


def send_response(wrong_tweet):
    if not wrong_tweet:
        return
    username = wrong_tweet.user.screen_name
    directmsg = "Recuerda @" + username + ": no se escribe 'phyton', sino 'python'!"
    replay_to_status_id = wrong_tweet.id
    twitter.tweet(message=directmsg, in_reply_to_status_id=replay_to_status_id)


if __name__ == "__main__":
    twitter = TwitterAPI()

    max_id = read_last_id()
    print (max_id)
    try:
        valid_tweet = None
        new_tweets = twitter.search(query="phyton", count=10, since_id=max_id + 1)
        tweet = None
        for tweet in reversed(new_tweets):
            valid, cause = is_valid(tweet)
            if valid:
                valid_tweet = tweet
                break
            else:
                print (cause, tweet.text)
        if valid_tweet:
            save_last_id(valid_tweet.id)
            print ('selected tweet: ', tweet.text)
            if (DIRECT_MSG_USER):
                send_direct_message(twitter, valid_tweet)
            else:
                send_response(valid_tweet)
        elif tweet:
            save_last_id(tweet.id)
    except tweepy.TweepError as e:
        print (e)
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        exit()
