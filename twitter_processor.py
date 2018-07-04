import ijson
import json
import unidecode
import re
import pytz
import os
from datetime import datetime
from tzwhere import tzwhere
from geopy.geocoders import Nominatim
from retrying import retry

def file_is_empty(path):
    return os.stat(path).st_size==0

#static current_timezone object to write on file
current_timezone = {}

def format_timezone(json_object, pytz_timezone):
    global current_timezone
    current_timezone['timezone_name'] = json_object['timezone']
    current_timezone['pytz_timezone'] = pytz_timezone


#list of timezones
timezones_list = []
timezones_aux_list = []
twitter_default_times_list = []
country_list = []

#file path for stopwords and json imports
#stopwords_file_path = 'stopwords.txt'
json_import_file_path = 'food_final3.json'
timezones_file_path = 'twitter_timezones.json'

#read files
#with open(stopwords_file_path) as f:
#    stopwords = f.read().splitlines()

with open(json_import_file_path, 'r') as f:
    objects = ijson.items(f, 'item')
    items = list(objects)

#load timezones using regular json line by line
timezones_file = open(timezones_file_path, 'a+')
if file_is_empty(timezones_file_path):
    pass
else:
    for line in timezones_file:
        try:
            timezone = json.loads(line)
            timezones_list.append(timezone)
        except:
            continue

print timezones_list[0]['country']
time_list = []
count = 0

print len(items)
import time


def localize_time(utctime, tzone):
    for asdf in timezones_list:
        if asdf['pytz_timezone'] == tzone:
            if asdf['country'] == 'None':
                return
            else:
                country_list.append(asdf['country'])
    current_date = datetime.strptime(utctime,'%Y-%m-%dT%H:%M:%SZ')
    timezone = pytz.timezone(tzone)
    localized_time = pytz.utc.localize(current_date, is_dst=None).astimezone(timezone)
    time_list.append(localized_time)
    global count
    count += 1
    #print 'Processed ' +  str(count) + ' items successfully!'

for idx, tweet in enumerate(items):
    if 'deals' in items[idx]['text'].lower():
        pass
    elif 'offers' in items[idx]['text'].lower():
        pass
    elif 'prizes' in items[idx]['text'].lower():
        pass
    elif 'lyft' in items[idx]['text'].lower():
        pass
    elif 'amazon' in items[idx]['text'].lower():
        pass
    elif 'drones' in items[idx]['text'].lower():
        pass
    elif 'RT @' in items[idx]['text']:
        pass
    elif items[idx]['timezone'] != None:
        #if timezones_list is not empty
        found_timezone = False
        if timezones_list:
            for timezone in timezones_list:
                if timezone['timezone_name'] == items[idx]['timezone']:
                    items[idx]['timezone'] = timezone['pytz_timezone']
                    localize_time(items[idx]['created_at'], items[idx]['timezone'])
                    found_timezone = True
                    break
        if not found_timezone:
            if items[idx]['timezone'] not in timezones_aux_list:
                format_timezone(items[idx], str(timezone))
                if '/' in items[idx]['timezone']:
                    current_timezone['pytz_timezone'] = items[idx]['timezone']
                else:
                    current_timezone['pytz_timezone'] = 'None'
                current_timezone['country'] = 'None'
                timezones_file.write(json.dumps(current_timezone))
                timezones_file.write('\n')
                timezones_aux_list.append(items[idx]['timezone'])
        else:
            pass


time_dict = {}
hour_list = []

for date in time_list:
    hour_list.append(date.hour)


for hour in hour_list:
    if hour in time_dict:
        time_dict[hour] += 1
    else:
        time_dict[hour] = 1

country_dict = {}
for country in country_list:
    if country in country_dict:
        country_dict[country] +=1
    else:
        country_dict[country] = 1


print '\n#########   Printing hourly traffic   #########\n'
for key, value in sorted(time_dict.iteritems(), reverse=True, key=lambda (k,v): (k,v)):
    print '%s: %s' % (key, value)

print '\n#########   Printing countries ordered by post volume   #########\n'
for key, value in sorted(country_dict.iteritems(), reverse=True, key=lambda (k,v): (v,k)):
    print '%s: %s' % (key, value)
