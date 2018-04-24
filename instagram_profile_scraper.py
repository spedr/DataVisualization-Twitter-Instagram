import urllib2
import sys
import json
from datetime import datetime
import time
from socket import error as SocketError
import errno
import unidecode
import re

link = sys.argv[1:][0]
link_name = link[:-4]
link_list = []
current_post = {}

with open(link) as f:
    for line in f:
        link_list.append(line)

jsonfile = open(link_name + '.json', 'w')

print len(link_list)

link_list = list(set(link_list))

print len(link_list)



def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def json_format(json_data):
    text = ""
    location_name = ""
    location_id = ""
    created_at = datetime.utcfromtimestamp(json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['taken_at_timestamp']).strftime('%Y-%m-%dT%H:%M:%SZ')
    username = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
    like_count = str(json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_preview_like']['count'])
    comment_count = str(json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['count'])
    if json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media'][ "edge_media_to_caption"]['edges']:
        text = remove_emoji(json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media'][ "edge_media_to_caption"]['edges'][0]['node']['text'])
        text = unidecode.unidecode(text)
        text = text.lower()
    if json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['location'] is not None :
        location_name =  json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['location']['name']
        location_id = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['location']['id']

    current_post['created_at'] = created_at
    current_post['username'] = username
    current_post['text'] = text
    current_post['like_count'] = like_count
    current_post['comment_count'] = comment_count
    current_post['location_name'] = location_name
    current_post['location_id'] = location_id

    print created_at
    print username
    print text
    print like_count
    print comment_count
    print location_name

    jsonfile.write(json.dumps(current_post))
    jsonfile.write(',')
    jsonfile.write('\n')



def get_info(item):
    try:
        response = urllib2.urlopen(item)
        page_source = response.read()
        from bs4 import BeautifulSoup, UnicodeDammit
        soup = BeautifulSoup(page_source, 'html.parser')

        data = soup.find_all('script', type='text/javascript')[2].text[21:][:-1]
        json_data = json.loads(data)
        json_format(json_data)

        time.sleep(1)
    except SocketError as e:
        pass
        time.sleep(10)
        get_info(item)
    except urllib2.HTTPError as err:
       if err.code == 404:
           pass
       else:
           pass
           time.sleep(10)
           get_info(item)
    except urllib2.URLError as err2:
        pass
        time.sleep(10)
        get_info(item)

for item in link_list:
    print item
    get_info(item)
