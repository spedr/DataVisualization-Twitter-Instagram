import ijson
from datetime import datetime

hashtag = '#food'
filename = "food3.json"


with open(filename, 'r') as f:
    objects = ijson.items(f, 'item')
    columns = list(objects)

##navigating json##
post_id = columns[0]['id']
created_at = datetime.utcfromtimestamp(columns[0]['edge_media_to_comment']['data'][0]['created_at'])
user_id = columns[0]['edge_media_to_comment']['data'][0]['owner']['id']
username = columns[0]['edge_media_to_comment']['data'][0]['owner']['username']
likes = columns[0]['edge_liked_by']['count']
comment_count = columns[0]['edge_media_to_comment']['count']
text = columns[0]['edge_media_to_caption']['edges'][0]['node']['text']

##localizing timezone##
from tzwhere import tzwhere
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim

geolocator = Nominatim()

location = geolocator.geocode(columns[0]['location']['name'])
tz = tzwhere.tzwhere(forceTZ=True)
current_location =  tz.tzNameAt(location.latitude, location.longitude)
timezone = pytz.timezone(current_location)
localized_timezone = pytz.utc.localize(created_at, is_dst=None).astimezone(timezone)
##end of timezone localization##


print post_id
print created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
print localized_timezone
print user_id
print username
print likes
print comment_count
print text

"""
import mysql.connector

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

for val in columns:
    data_entry = {
      'ID': columns[it]['id'],
      'social_network': 1,
      'user_id': 0,
      'user_name': columns[it]['username'],
      'screen_name': columns[it]['userscreen_name'],
      'number_followers': 0,
      'hashtag': hashtag,
      'text_content': columns[it]['edge_media_to_caption']['edges'][0]['node']['text'],
      'date_time': datetime.utcfromtimestamp(columns[it]['edge_media_to_comment']['data'][0]['created_at']),
      'likes': columns[it]['edge_liked_by']['count'],
      'retweets': columns[it]['retweet_count'],
      'number_comments': 0,
      'timezone': 0,
      'updated': 0
    }
    cursor.execute(add_entry, data_entry)
    it+=1

cnx.commit()
cursor.close()
cnx.close()
"""
