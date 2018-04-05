import tweepy
from tweepy import OAuthHandler

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_token_key"], config["access_token_secret"])

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

#get ID from database

#tweet = api.get_status(tweet_id)


#for tweet in tweepy.Cursor(api.search,q="#ps4",count=100,\
#                           lang="en",\
#                           until="2018-03-25").items():
#    print tweet.created_at, tweet.text
