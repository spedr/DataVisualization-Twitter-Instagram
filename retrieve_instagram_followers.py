import urllib, json
ig_username = "kinoconomori"
url = "http://instagram.com/" + ig_username + "/?__a=1"
response = urllib.urlopen(url)
data = json.loads(response.read())
print data['graphql']['user']['edge_followed_by']['count']
