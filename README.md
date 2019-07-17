# TweetReplyAnalyzer
Get counts of keywords that appear in the replies of a specific tweet

Made on Python 2.7, but can easily be modified to work on Python 3.x

# How to Use

Replace `TwitterHandle` and `StatusID` with what appears in the URL of the tweet you want to analyze (`https://twitter.com/`**TwitterHandle**`/status/`**StatusID**) on line 83

https://github.com/FlyingKatsu/TweetReplyAnalyzer/blob/875c265c8159dd87849049a966ceb106a358c935/index.py#L83


Add your keyword aliases to the dictionary on lines 88-94

https://github.com/FlyingKatsu/TweetReplyAnalyzer/blob/875c265c8159dd87849049a966ceb106a358c935/index.py#L88-L94


Add your keys, tokens, and secrets to the authentication on lines 12-16. See https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens for help creating these values.

https://github.com/FlyingKatsu/TweetReplyAnalyzer/blob/875c265c8159dd87849049a966ceb106a358c935/index.py#L12-L16
