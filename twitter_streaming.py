import json
config = json.load(open('config.json'))

#Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_token_key"], config["access_token_secret"])

queue = open('queue.json','w')
hashtag = '#food'
current_tweet = {}



#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    counter = 0

    @staticmethod
    def json_format(data_json):
        current_tweet['social_network'] = 0
        current_tweet['id'] = data_json['id']
        current_tweet['created_at'] = data_json['created_at']
        current_tweet['userid'] = data_json['user']['id']
        current_tweet['username'] = data_json['user']['name']
        current_tweet['number_followers'] = data_json['user']['followers_count']
        current_tweet['userscreen_name'] = data_json['user']['screen_name']
        current_tweet['usertimezone'] = data_json['user']['time_zone']
        current_tweet['retweet_count'] = data_json['retweet_count']
        current_tweet['favorite_count'] = data_json['favorite_count']
        current_tweet['hashtag'] = hashtag
        current_tweet['text'] = data_json['text']
        current_tweet['updated'] = 0
        return

    def on_data(self, data):
        data_json = json.loads(data)
        print data_json['user']['name']
        print data_json['user']['screen_name']
        print data_json['user']['time_zone']
        self.json_format(data_json)

        queue.write(json.dumps(current_tweet))
        queue.write('\n')
        self.counter+=1
        print 'Number of tweets collected so far...: ' , self.counter
        return True

    def on_error(self, status):
        print status






if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=[hashtag])
