"""Generate Markov text from text files."""

from random import choice
from sys import argv
import twitter
import os

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path) as text:
        text_str = text.read()

    return text_str


def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    word_lst = text_string.split()

    for i in range(len(word_lst) - 1):
        curr_tuple = tuple(word_lst[i:i+n])
        # print curr_tuple
        try:
            if curr_tuple in chains:
                chains[curr_tuple].append(word_lst[i + n])
            else:
                chains[curr_tuple] = [word_lst[i + n]]
        except IndexError:
            if curr_tuple in chains:
                chains[curr_tuple].append(None)                 
            else:
                chains[curr_tuple] = [None]
    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    while True:
        chosen_key = choice(chains.keys())

        if chosen_key[0][0].isupper():
            break
        else:
            continue


    chosen_value = choice(chains[chosen_key])

    words.append(chosen_key[0])

    while True:
        chosen_key = chosen_key[1:n] + (chosen_value,)
        try:
            chosen_value = choice(chains[chosen_key])
        except KeyError:
            words.extend(list(chosen_key[0:n-1]))
            break

        words.append(chosen_key[0])

    joined_words = " ".join(words)
    tweet_str = joined_words[:140]
    return tweet_str

def tweet(tweet_str):
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

    status = api.PostUpdate(tweet_str)
    print status.text

    # user_confirmation = raw_input("Enter to tweet again [q to quit] > ")

    # if user_confirmation.lower() == 'q':
    #     break
    # else:
        


input_path = argv[1]
n = int(argv[2])

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, n)

# Produce random text
random_text = make_text(chains)

print random_text

tweets = tweet(random_text)
