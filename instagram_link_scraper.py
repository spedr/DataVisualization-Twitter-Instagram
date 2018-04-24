import urllib2
import sys
import json
import time

link = sys.argv[1:][0]

tag = link

link = 'https://www.instagram.com/explore/tags/' + link

to_scrape = open('to_scrape_' + tag + '.txt','a+')


while True:
    try:
        response = urllib2.urlopen(link)
        page_source = response.read()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')


        data = soup.find_all('script', type='text/javascript')[2].text[21:][:-1]
        #print data

        json_data = json.loads(data)



        post_list =  json_data['entry_data']['TagPage'][0]['graphql']['hashtag']["edge_hashtag_to_media"]["edges"]

        for post in post_list:
            to_scrape.write('https://www.instagram.com/p/' + post['node']["shortcode"])
            to_scrape.write('\n')

    except SocketError as e:
        if error.errno == errno.WSAECONNRESET:
            pass
            time.sleep(30)
        if e.errno != errno.ECONNRESET:
            raise
        pass
    time.sleep(15)
