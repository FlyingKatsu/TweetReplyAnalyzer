# NOTE: This runs on Python 2.7, not 3.x
import string
import itertools
import collections
import os
from enum import Enum
# pip install tweepy
import tweepy
from tweepy import OAuthHandler
# pip install nltk
# python -m nltk.downloader stopwords
from nltk.corpus import stopwords

# ===========================================================
#        Configuration
# ===========================================================

# Make sure to set these values in a copy of secret.sample.py and run `python start.py`
# Alternatively, if on a private server, set the variables manually via shell: `export VAR='value'`
class Auth():
  consumer_key = os.getenv('TwitterReplyAnalyzer_ConsumerKey', None)
  consumer_secret = os.getenv('TwitterReplyAnalyzer_ConsumerSecret', None)
  access_token = os.getenv('TwitterReplyAnalyzer_AccessToken', None)
  access_secret = os.getenv('TwitterReplyAnalyzer_AccessSecret', None)

# Set up configuration
class TweetConfig():
  author = 'TwitterHandle'
  tweet_id = '0000000000'
  max_results = 500
  max_top_count = 100

# Initialize our options
class Options(Enum):
  Option_1 = 1
  Option_2 = 2
  Option_3 = 3

# Initialize aliases for each option
# Any text that matches the values in the array will be replaced with the name of the option
option_aliases = {
  Options.Option_1.name: [
    'one',
    '1'
  ],

  Options.Option_2.name: [
    'two', 
    '2', 
  ],

  Options.Option_2.name: [
    'three', 
    '3', 
  ],
}

# Initialize buckets for each option
global_options = [ name for name, member in Options.__members__.items() ]
global_dict = { k:[] for k in global_options }
global_aliases = { alias:key for key in option_aliases for alias in option_aliases[key] }
# print(global_aliases)
# print(global_dict)

# ===========================================================
#        Helper Methods
# ===========================================================

def create_authenticated_api():
  # Authentication
  auth = OAuthHandler(Auth.consumer_key, Auth.consumer_secret)
  auth.set_access_token(Auth.access_token, Auth.access_secret)

  return tweepy.API(auth, wait_on_rate_limit=True)

def get_replies_to_tweet(api, tweet_author, tweet_id, max):
  # Get replies to specific user's tweet
  tweet_author_q = 'to:' + tweet_author
  replies = []

  tweet_op = api.get_status(tweet_id, tweet_mode='extended')
  print('Original Tweet by @' + tweet_author + ': ' + tweet_op.full_text.encode('ascii', 'ignore') + '\n')
  
  for tweet in tweepy.Cursor(api.search, q=tweet_author_q, since_id=tweet_id, result_type='recent', tweet_mode='extended', timeout=999999).items(max):
    if hasattr(tweet,'in_reply_to_status_id_str'):
      if(tweet.in_reply_to_status_id_str==tweet_op.id_str):
        replies.append(tweet.full_text.encode('ascii', 'ignore'))

  return replies

def replace_aliases(text, aliases):
  words = []

  for word in text.split():
    if aliases.get(word):
      words.append(aliases.get(word))
    else:
      words.append(word)

  return words

def clean_reply_text(tweets, aliases, filter_with_stopwords=True):
  words = []

  if filter_with_stopwords:
    stop_words = set(stopwords.words('english'))
    # print(list(stop_words)[0:10])

  for reply in tweets:
    # Remove punctuation, convert case
    translator = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    reply_clean = reply.translate(translator).lower()
    # Replace alias words (a = alpha, 1 = one, etc.)
    reply_words = replace_aliases(reply_clean, aliases)
    # Remove duplicate words from tweet
    reply_words = list( dict.fromkeys(reply_words) )
    # Remove unimportant words
    if filter_with_stopwords:
      reply_words = [ word for word in reply_words if not word in stop_words ]
    # Keep track of which replies mention which named options
    for name in global_options:
      try:
        if reply_words.index(name) >= 0:
          global_dict[name].append(reply)
      except ValueError:
        pass
    # Add to result
    words.append(reply_words)

  return words

def get_word_counts(words):
  # Flatten list
  all_words = list(itertools.chain(*words))
  # Get word frequencies
  counts = collections.Counter(all_words)

  # Return top 100 words
  count_file = open('output/count.txt','w')
  for count in counts.most_common(TweetConfig.max_top_count):
    count_file.write(' '.join(str(s) for s in count) + '\n')
  count_file.close

if __name__ == '__main__':
  print('Beginning the mission...\n')
  
  api = create_authenticated_api()
  replies = get_replies_to_tweet(api, TweetConfig.author, TweetConfig.tweet_id, TweetConfig.max_results)

  # print(replies)
  reply_file = open('output/replies.txt','w')
  for reply in replies:
    reply_file.write('"' + reply.replace('\n', ' ') + '"\n')
  reply_file.close
  
  reply_words = clean_reply_text(replies, global_aliases, True)
  get_word_counts(reply_words)

  # print(global_dict)
  for name in global_options:
    word_file = open('output/buckets/'+ name +'.json', 'w')
    lines = global_dict.get(name)
    word_file.write('{\n"' + name + '": {\n')
    word_file.write('"count": ' + str(len(lines)) + ',\n')
    word_file.write('"replies": [\n')
    for line in lines:
      word_file.write('"' + line.replace('\n',' ') + '",\n')
    word_file.write(']\n}\n}\n')
    word_file.close

  print('\nProcessed ' + str(len(replies)) + ' replies to original tweet.\n')