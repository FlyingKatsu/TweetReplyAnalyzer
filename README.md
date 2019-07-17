# TweetReplyAnalyzer
Get counts of keywords that appear in the replies of a specific tweet

Made on Python 2.7, but can easily be modified to work on Python 3.x

# How to Use

1. Copy, clone, or download this repo.

2. Install packages
    1. `pip install tweepy`
    2. `pip install nltk`
    3. `python -m nltk.downloader stopwords`

3. On [line 83](https://github.com/FlyingKatsu/TweetReplyAnalyzer/blob/875c265c8159dd87849049a966ceb106a358c935/index.py#L83), replace `TwitterHandle` and `StatusID` with what appears in the URL of the tweet you want to analyze `https://twitter.com/`**TwitterHandle**`/status/`**StatusID**

4. Add your keyword aliases to the dictionary on [lines 88-94](https://github.com/FlyingKatsu/TweetReplyAnalyzer/blob/875c265c8159dd87849049a966ceb106a358c935/index.py#L88-L94)

5. Add your keys, tokens, and secrets to the authentication on [lines 12-16](https://github.com/FlyingKatsu/TweetReplyAnalyzer/blob/875c265c8159dd87849049a966ceb106a358c935/index.py#L12-L16). See [Twitter Developer Docs](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens) for help creating these values.
