import re
import os
import json
import sys, getopt
import time
from random import randint
def generateJsonUsers(inputfile, outputfile):
    idUserList = []
    with open(inputfile) as json_data:
      tweets = json.load(json_data)
    results = averagesAndTotals(inputfile)
    file  = open(outputfile, "a+")
    file.write("[")    
    for index in range(len(tweets)):
        tweet = tweets[index]
        if tweet["userid"] not in idUserList:            
            idUserList.append(tweet["userid"])
            #originalFollowers = tweet["followers_count"]
            retweetsTotal = tweet["retweet_count"]
            likesTotal = tweet["favorite_count"]
            number_of_tweets = 1
            #raiseOfFollowers = False
            #finalFollowers = tweet["followers_count"]
            for index2 in range(index+1, len(tweets)):
                tweUs = tweets[index2]                
                if tweet["userid"] == tweUs["userid"]:
                    number_of_tweets += 1                    
                    retweetsTotal += tweUs["retweet_count"]
                    likesTotal += tweUs["favorite_count"]
                    #if raiseOfFollowers is True and finalFollowers < tweUs["followers_count"]:
                        #finalFollowers = tweUs["followers_count"]
                    #elif tweUs["followers_count"] > originalFollowers:
                        #raiseOfFollowers = True
                        #finalFollowers = tweUs["followers_count"]
            averageRetweets = retweetsTotal/number_of_tweets
            averageLikes = likesTotal/number_of_tweets
            influence_level = 0            
            if (results["Average likes"] < averageLikes and results["Average retweets"] > averageRetweets):
                influence_level = 1
            if (results["Average likes"] > averageLikes and results["Average retweets"] < averageRetweets):
                influence_level = 1
            if results["Average likes"] < averageLikes and results["Average retweets"] < averageRetweets and number_of_tweets >= 2:
                influence_level = 2
            #raisedFollowers = 0
            #if raiseOfFollowers is True:
                #raisedFollowers = 1
            file.write("{\n" + "	\"userid\": \""+str(tweet["userid"])+"\",\n"+	  								
                                          #  "	\"hashtags\": \""+ tweet["hashtags"] +"\",\n" +
                                            "	\"number_of_tweets\": " + str(number_of_tweets) +"," + "\n"+
                                            "	\"retweet_count_total\": " + str(retweetsTotal) +", \n" +
                                            "	\"average_retweet_count\": " + str(averageRetweets) +",\n" +
                                            #"	\"followers_count\": " + str(originalFollowers) +",\n" +
                                            #"    \"followers_count_increased\": "+ str(raisedFollowers) + ",\n"+
                                            #"    \"final_followers_count\": "+ str(finalFollowers) + ",\n" +
                                            "	\"total_likes\": " + str(likesTotal) +",\n" +
                                            "    \"average_likes\": " + str(averageLikes) +",\n"+
                                            "    \"influence_level\": "+ str(influence_level) +""+
                                            #"    \"total_users\": "+str(number_of_users) +""+
                                            "\n},\n")
    file.write("\n]")
    file.close()

def averagesAndTotals(inputfile):
    with open(inputfile) as json_data:
      tweets = json.load(json_data)
    allLikes = 0
    allRetweets = 0
    averageLikes = 0
    averageRetweets = 0
    #totalFollowers = 0
    #averageFollowers = 0
    number_of_tweets = 0
    number_of_users = 0    
    idUserList = []
    print("ok")
    for tweet in tweets:
        allLikes += tweet["favorite_count"]
        allRetweets += tweet["retweet_count"]
        number_of_tweets += 1        
        if number_of_tweets%1000 == 0:
            print(number_of_tweets)
        if tweet["userid"] not in idUserList:
            number_of_users += 1
            idUserList.append(tweet["userid"])
            #totalFollowers += tweet["followers_count"]            
    averageLikes = allLikes/number_of_tweets
    averageRetweets = allRetweets/number_of_tweets
    #averageFollowers = totalFollowers/number_of_users
    averageNumberOfTweetsPerUser = number_of_tweets/number_of_users
    results = {"Number of tweets":number_of_tweets, "Number of users":number_of_users,
    "Average number of tweets per user":averageNumberOfTweetsPerUser,
    "All likes":allLikes,"Average likes":averageLikes,
    "All retweets":allRetweets,"Average retweets":averageRetweets}
    #"Average followers":averageFollowers}
    print("Number of tweets: ", number_of_tweets)
    print("Number of users: ", number_of_users)
    print("Average number of tweets per user: ", averageNumberOfTweetsPerUser)
    print("All likes: ", allLikes)
    print("Average likes: ", averageLikes)
    print("All retweets: ", allRetweets)
    print("Average retweets: ", averageRetweets)
    return results


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
   start_time = time.time()
   #averagesAndTotals(inputfile)
   generateJsonUsers(inputfile, outputfile)
   print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
   main(sys.argv[1:])