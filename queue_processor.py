import json
import mysql.connector
import pandas as pd
from dateutil import parser

tweets_data_path = 'queue.json'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

cnx = mysql.connector.connect(user='root', password='tc2',
                                host='127.0.0.1',
                                database='tc2')




add_entry = ("INSERT INTO Entry "
               "(ID, social_network, user_id, user_name, screen_name, number_followers, hashtag, text_content, date_time, likes, retweets, number_comments, timezone, updated) "
               "VALUES (%(ID)s, %(social_network)s, %(user_id)s, %(user_name)s, %(screen_name)s, %(number_followers)s, %(hashtag)s, %(text_content)s, %(date_time)s, %(likes)s, %(retweets)s, %(number_comments)s, %(timezone)s, %(updated)s)")

it = 0

cursor = cnx.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")

print parser.parse(tweets_data[it]['created_at'])

for val in tweets_data:
    data_entry = {
      'ID': tweets_data[it]['id'],
      'social_network': tweets_data[it]['social_network'],
      'user_id': tweets_data[it]['userid'],
      'user_name': tweets_data[it]['username'],
      'screen_name': tweets_data[it]['userscreen_name'],
      'number_followers': tweets_data[it]['number_followers'],
      'hashtag': tweets_data[it]['hashtag'],
      'text_content': tweets_data[it]['text'],
      'date_time': parser.parse(tweets_data[it]['created_at']),
      'likes': tweets_data[it]['favorite_count'],
      'retweets': tweets_data[it]['retweet_count'],
      'number_comments': 0,
      'timezone': tweets_data[it]['usertimezone'],
      'updated': 0
    }
    print tweets_data[it]['text']
    cursor.execute(add_entry, data_entry)
    it+=1








# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()

print tweets_data[0]['username']
