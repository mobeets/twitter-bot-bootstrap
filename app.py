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

def random_favoriting(keywords, handle, favorite_probability=0.2):
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

def get_urls_of_media_in_tweet(tweet):
    """
    get the urls of media contained in a tweet
    """
    if 'entities' not in tweet or 'media' not in tweet['entities']:
        return []
    return [x['media_url'] for x in tweet['entities']['media']]

def get_mentions(handle, include_entities=False):
    """
    returns iterator of tweets mentioning us
        if you want to get media in tweets, include_entities must be True
    """
    return handle.cursor(handle.get_mentions_timeline,
        include_entities=include_entities)

def get_images_in_mentions(handle):
    """
    check for tweets that mention you, and get the urls of media in those tweets

    e.g., this might be helpful if you make a twitter bot where users can mention you in tweets containing photos, and your bot replies with an altered version of that photo
    """
    for tweet in get_mentions(handle, include_entities=True):
        urls = get_urls_of_media_in_tweet(tweet)
        yield urls

def submit_tweet_with_media(message, mediafile, tweet_to_reply=None, handle=None):
    """
    imfile is the path to an media
    tweet_to_reply is a tweet that you're replying to, if not None
    """
    if not handle:
        handle = twitter_handle()
    media_ids = handle.upload_media(media=open(mediafile))
    if tweet_to_reply is None:
        handle.update_status(status=message,
            media_ids=media_ids['media_id'])
    else:
        # must mention user's name for it to be a reply
        message += ' @' + tweet_to_reply['user']['screen_name']
        handle.update_status(status=message,
            in_reply_to_status_id=tweet_to_reply['id'],
            media_ids=media_ids['media_id'])

def submit_tweet(message, tweet_to_reply=None, handle=None):
    """
    tweet_to_reply is a tweet that you're replying to, if not None
    """
    if not handle:
        handle = twitter_handle()
    if tweet_to_reply is None:
        handle.update_status(status=message)
    else:
        # must mention user's name for it to be a reply
        message += ' @' + tweet_to_reply['user']['screen_name']
        handle.update_status(status=message,
            in_reply_to_status_id=tweet_to_reply['id'])

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
