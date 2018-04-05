import re
import os
import json
import sys, getopt
from datetime import datetime

def toArff(inputfile, outputfile):
  with open(inputfile) as json_data:
      tweets = json.load(json_data)
      

  file  = open(outputfile, "a+")
  file.write('''@RELATION tweets
  @ATTRIBUTE id string
  @ATTRIBUTE date_time DATE "yyyy-MM-dd HH:mm:ss"
  @ATTRIBUTE hashtags string
  @ATTRIBUTE retweet {'y', 'n'}
  @ATTRIBUTE retweet_count numeric
  @ATTRIBUTE followers_count numeric
  @ATTRIBUTE likes numeric
  @ATTRIBUTE text_content string


  @DATA
  ''');

  for tweet in tweets:
    retweet_count = tweet["retweet_count"]
    followers_count = tweet["followers_count"]
    likes = tweet["likes"]

    date = datetime.strptime(str(tweet["date_time"]), '%a %b %d %H:%M:%S %Y')
    dateFormat = date.strftime('%Y-%m-%d %H:%M:%S')
    
    file.write("\n'" +tweet["id"] +
        "',\"" +dateFormat + 
        "\",'" +tweet["hashtags"] +
        "','" +tweet["retweet"] +
        "'," +str(retweet_count) +
        "," +str(followers_count) +
        "," +str(likes) +
        ",'" +tweet["text_content"]+"'")


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print 'Input file is "', inputfile
   print 'Output file is "', outputfile
   toArff(inputfile, outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])
