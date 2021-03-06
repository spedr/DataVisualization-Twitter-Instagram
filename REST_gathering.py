import tweepy
from tweepy import OAuthHandler
import json
import logging
import time

config = json.load(open('config.json'))
auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_token_key"], config["access_token_secret"])

api = tweepy.API(auth)


queue = open('food_final2.json','w')

queue.write('[')

current_tweet = {}

def json_format(data_json):
    current_tweet['id'] = data_json.id
    current_tweet['timezone'] = data_json.user.time_zone
    current_tweet['created_at'] = data_json.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
    current_tweet['userid'] = data_json.user.id
    current_tweet['username'] = data_json.user.name
    current_tweet['screen_name'] = data_json.user.screen_name
    current_tweet['retweet_count'] = data_json.retweet_count
    current_tweet['favorite_count'] = data_json.favorite_count
    current_tweet['text'] = data_json.text
    current_tweet['lang'] = data_json.lang

    return

counter = 0
c = 0
#bbb search terms
#search_terms = '"#BBB18" OR "kaysar" OR "gleici" OR "#gleicicampea" OR "#timegleici" OR "#timekaysar" OR "#teamkaysar" OR "#finalbbb18" OR "redebbb" OR "big brother brasil" OR "ana clara"'
search_terms = '"#food"'


#last_id = 984834833032491008 old
#id2 = 982928355287855105
#bbb ids
#last_id = 987234644767600640
#id2 = 987088251700809728

#food2 ids
last_id = 988466935120744448
id2 = 983068971418243072

while True:
    try:
        new_tweets = api.search(q = search_terms, count=100, include_entities=True,monitor_rate_limit=True,wait_on_rate_limit=True,wait_on_rate_limit_notify = True,retry_count = 5,retry_delay = 5, since_id=str(id2), max_id=str(last_id-1))
        if not new_tweets:
            break
        for tweet in new_tweets:
            json_format(tweet)
            queue.write(json.dumps(current_tweet))
            queue.write(',\n')
            counter+=1
            print 'Number of tweets collected so far...: ', counter
        last_id = new_tweets[-1].id
    except Exception, e:
        continue
    time.sleep(3.5)

queue.close()

#for tweet in tweepy.Cursor(api.search, q = search_terms, count=100, include_entities=True,monitor_rate_limit=True,wait_on_rate_limit=True,wait_on_rate_limit_notify = True,retry_count = 5,retry_delay = 5, since = start_since, until= end_until,lang='pt').items():
#	try:
#		json_format(tweet)
#		queue.write(json.dumps(current_tweet))
#		counter+=1
#		print 'Number of tweets collected so far...:' , counter
#		queue.write('\n')
#	except Exception, e:
#		#log.error(e)
#		logging.exception("message")
#	c+=1
#	if c % 100 == 0:
#		time.sleep(5)
