import string
import itertools
import collections
# pip install tweepy
import tweepy
from tweepy import OAuthHandler
# pip install nltk
# python -m nltk.downloader stopwords
from nltk.corpus import stopwords

def create_authenticated_api():
  # Authentication
  consumer_key = ''
  consumer_secret = ''
  access_token = ''
  access_secret = ''

  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  return tweepy.API(auth, wait_on_rate_limit=True)

def get_replies_to_tweet(api, tweet_author, tweet_id):
  # Get replies to specific user's tweet
  tweet_author_q = 'to:' + tweet_author
  replies = []

  tweet_op = api.get_status(tweet_id, tweet_mode='extended')
  print('Original Tweet by @' + tweet_author + ': ' + tweet_op.full_text.encode('ascii', 'ignore') + '\n')
  
  for tweet in tweepy.Cursor(api.search, q=tweet_author_q, since_id=tweet_id, result_type='recent', tweet_mode='extended', timeout=999999).items(200):
    if hasattr(tweet,'in_reply_to_status_id_str'):
      if(tweet.in_reply_to_status_id_str==tweet_op.id_str):
        replies.append(tweet.full_text.encode('ascii', 'ignore'))

  return replies

def replace_aliases(list, aliases):
  words = []

  for word in list:
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
    reply = reply.translate(translator).lower()
    # Replace alias words (a = alpha, 1 = one, etc.)
    reply_words = replace_aliases(reply.split(), aliases)
    # Remove duplicate words from tweet
    reply_words = list( dict.fromkeys(reply_words) )
    # Remove unimportant words
    if filter_with_stopwords:
      reply_words = [ word for word in reply_words if not word in stop_words ]
    # Add to result
    words.append(reply_words)

  return words

def get_word_counts(words):
  # Flatten list
  all_words = list(itertools.chain(*words))
  # Get word frequencies
  counts = collections.Counter(all_words)
  # Return top 50 words
  print(counts.most_common(50))


if __name__ == '__main__':
  api = create_authenticated_api()
  replies = get_replies_to_tweet(api, 'TwitterHandle', 'StatusID')

  # Raw text data
  print(replies)

  # Filter text for better results
  # 'key' : 'value'
  # key is what appears in text
  # value is what key should be replaced with
  aliases = {
    'key': 'value',
  }
  
  # Results with nltk stopword filter
  get_word_counts( clean_reply_text(replies, aliases, True) )
  # Results without nltk stopword filter
  get_word_counts( clean_reply_text(replies, aliases, False) )
 
