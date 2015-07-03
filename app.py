import os
import time
from random import random
from twython import Twython

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['TWITTER_OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['TWITTER_OAUTH_TOKEN_SECRET']
TWEET_LENGTH = 140
TWEET_URL_LENGTH = 21

RUN_EVERY_N_SECONDS = 60*5 # e.g. 60*5 = tweets every five minutes

USERS_TO_IGNORE = []
DO_NOT_FAVORITE_USERS_AGAIN = True

def twitter_handle():
    return Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def favorite_tweet(tweet, handle):
    handle.create_favorite(id=tweet['id'])

def random_favoriting(keywords, handle, favorite_probability=0.5):
    """
    keywords is a list, like ['bananas', 'apples', 'oranges']

    n.b. if this function is called every N seconds
        then you can expect to favorite a tweet
        once every N/favorite_probability seconds
    """
    for keyword in keywords:
        xs = handle.search(q=keyword)
        ts = [x for x in xs['statuses']]
        if DO_NOT_FAVORITE_USERS_AGAIN:
            ts = [x for x in ts if x['user']['id'] not in USERS_TO_IGNORE]
        if ts:
            if random() < favorite_probability: 
                print 'Favoriting: ' + ts[0]['text']
                favorite_tweet(ts[0], handle)
                if DO_NOT_FAVORITE_USERS_AGAIN:
                    USERS_TO_IGNORE.append(ts[0]['user']['id'])
                return

def submit_tweet(message, handle=None):
    if not handle:
        handle = twitter_handle()
    handle.update_status(status=message)

def get_message(handle):
    """
    Your code goes here!
    """
    message = 'I TWEET THIS.'
    assert len(message) <= TWEET_LENGTH
    return message

def main():
    handle = twitter_handle()
    USERS_TO_IGNORE.extend([x['user']['id'] for x in handle.get_favorites()])
    while True:
        message = get_message(handle)
        print message
        submit_tweet(message, handle)
        # random_favoriting(['apples', 'oranges'], handle)
        time.sleep(RUN_EVERY_N_SECONDS)

if __name__ == '__main__':
    main()
