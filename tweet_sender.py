# from random import choice
# from sys import argv
import twitter
import os
from markov import *

def tweet(chains):
    """Create a tweet and send it to the Internet."""

    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    while True:
        random_text = make_text(chains)
        print random_text

        to_tweet_or_not = raw_input("Do you want to tweet this? (y/n) > ")

        if to_tweet_or_not == "n":
            continue
        else:    
            status = api.PostUpdate(random_text)
            print "Confirmed tweet: " + status.text

            user_confirmation = raw_input("Enter to tweet again [q to quit] > ")

            if user_confirmation.lower() == 'q':
                break


tweets = tweet(chains)
