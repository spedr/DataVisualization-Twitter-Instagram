import ijson
from datetime import datetime


filename = "food.json"


with open(filename, 'r') as f:
    objects = ijson.items(f, 'item')
    columns = list(objects)

post_id = columns[0]['id']
created_at = datetime.utcfromtimestamp(columns[0]['edge_media_to_comment']['data'][0]['created_at'])
username = columns[0]['edge_media_to_comment']['data'][0]['owner']['username']
likes = columns[0]['edge_liked_by']['count']
comment_count = columns[0]['edge_media_to_comment']['count']
text = columns[0]['edge_media_to_caption']['edges'][0]['node']['text']

print post_id
print created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
print username
print likes
print comment_count
print text
