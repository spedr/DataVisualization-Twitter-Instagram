from tzwhere import tzwhere
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim

geolocator = Nominatim()
location = geolocator.geocode('Sydney, Australia')
tz = tzwhere.tzwhere(forceTZ=True)
print location.latitude
print location.longitude

posix_timestamp = 1521327698
utc_time = datetime.utcfromtimestamp(posix_timestamp)
current_location =  tz.tzNameAt(location.latitude, location.longitude)

timezone = pytz.timezone(current_location)

print utc_time
print pytz.utc.localize(utc_time, is_dst=None).astimezone(timezone)
