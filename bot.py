import os
import tweepy
from dotenv import load_dotenv
import json

# Load the required env variables. Check README.md and .env.example for help.
load_dotenv()

consumer_key = os.getenv('CONSUMER_API_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)


def is_valid_member(tweet):
    """ Checks if the account that called the bot has the correct permisions. """
    return True


def fetch_target_tweet(tweet):
    """ Returns the tweet to archive from the tweet that activated the bot. """
    target_id = tweet.in_reply_to_status_id
    target_tweet = api.get_status(target_id, tweet_mode="extended")
    return target_tweet


def archive(tweet):
    target_tweet = fetch_target_tweet(tweet)
    print(target_tweet)


def process_tweet(tweet):
    if is_valid_member(tweet):
        archive(tweet)
    else:
        # Tweet at them that they need to join our dao to use us.
        pass


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        process_tweet(tweet)
        print(json.dumps(tweet._json))

    def on_error(self, status):
        print("Error detected")


# Create stream to listen all tweets related to @watchdogdao
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(follow=["1280934313073299456"])
