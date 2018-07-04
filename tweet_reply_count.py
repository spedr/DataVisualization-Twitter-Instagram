import urllib2

twitter_username = 'TwitterDev'
tweet_id = 850006245121695744


response = urllib2.urlopen("https://twitter.com/"+ twitter_username + "/status/" + str(tweet_id))
page_source = response.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

print soup.find_all(id='profile-tweet-action-reply-count-aria-' + str(tweet_id))[0].text.partition(' ')[0]
