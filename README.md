# TweetReplyAnalyzer
Get counts of keywords that appear in the replies of a specific tweet.

Made on Python 2.7, but can easily be modified to work on Python 3.x

## How to Use

1. Copy, clone, or download this repo.

2. Install packages
    1. `pip install tweepy`
    2. `pip install nltk`
    3. `python -m nltk.downloader stopwords`

3. On lines 26 through 31 of `main.py`, replace `TwitterHandle` and `000000000` with what appears in the URL of the tweet you want to analyze `https://twitter.com/`**TwitterHandle**`/status/`**StatusID**

4. Define your option buckets on lines 35 through 37 of `main.py`. Add as many as you need. 

5. For each of your option buckets, add synonyms to the aliases dictionary on lines 41 through 56 of `main.py`. Add as many as you need, but make sure each synonym is a single, lowercase word with no punctuation (as these will be compared against filtered, split text).

6. Copy `secret.sample.py` and add your keys, tokens, and secrets according to the Twitter App you create. See [Twitter Developer Docs](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens) for more info.

7. Run `python start.py` which will load your environment variables in `secret.py` and then run `main.py`. Check the `output` directory for results.


## How it works

Generally, it collects all (up to `TweetConfig.max_results` most recent) replies to the given `TweetConfig.tweet_id`. For each reply, it removes punctuation, sets to lowercase, separates words, replaces synonyms with one of the bucket names (ex: `one` and `1` become `Option_1`), and removes duplicates within the same reply.

Finally it outputs the resulting counts in descending order, along with buckets for each voting option. The buckets contain every unmodified reply that was counted towards the voting option, so that it can be manually reviewed and results adjusted for errors. 

Each bucket is output as its own `output/buckets/Bucket_Name.json` file. A full list of the reply texts is output in `output/replies.txt`, which is useful for comparing results from different days via diff. Newest results are on top. The top `TweetConfig.max_top_count` words are listed in `output/count.txt`