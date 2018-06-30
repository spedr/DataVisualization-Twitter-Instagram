import re
import os
import json
import sys, getopt
import time
from random import randint
def generateJsonUsers(inputfile, outputfile):
    usernameList = []
    with open(inputfile) as json_data:
      posts = json.load(json_data)
    results = averagesAndTotals(inputfile)
    file  = open(outputfile, "a+")
    file.write("[")    
    for index in range(len(posts)):
        post = posts[index]
        if post["username"] not in usernameList:            
            usernameList.append(post["username"])
            
            commentsTotal = int(post["comment_count"])
            likesTotal = int(post["like_count"])
            number_of_posts = 1           
            for index2 in range(index+1, len(posts)):
                posUs = posts[index2]                
                if post["username"] == posUs["username"]:
                    number_of_posts += 1                    
                    commentsTotal += int(posUs["comment_count"])
                    likesTotal += int(posUs["like_count"])
            averageComments = commentsTotal/number_of_posts
            averageLikes = likesTotal/number_of_posts
            influence_level = 0            
            if (results["Average likes"] < averageLikes and results["Average comments"] >= averageComments):
                influence_level = 1
            if (results["Average likes"] >= averageLikes and results["Average comments"] < averageComments):
                influence_level = 1
            if results["Average likes"] < averageLikes and results["Average comments"] < averageComments:
                influence_level = 2            
            file.write("{\n" + "	\"username\": \""+post["username"]+"\",\n"+	  								
                                          #  "	\"hashtags\": \""+ post["hashtags"] +"\",\n" +
                                            "	\"number_of_posts\": " + str(number_of_posts) +"," + "\n"+
                                            "	\"comments_count_total\": " + str(commentsTotal) +", \n" +
                                            "	\"average_comments_count\": " + str(averageComments) +",\n" +                                           
                                            "	\"total_likes\": " + str(likesTotal) +",\n" +
                                            "    \"average_likes\": " + str(averageLikes) +",\n"+
                                            "    \"influence_level\": "+ str(influence_level) +""+
                                            #"    \"total_users\": "+str(number_of_users) +""+
                                            "\n},\n")
    file.write("\n]")
    file.close()

def averagesAndTotals(inputfile):
    with open(inputfile) as json_data:
      posts = json.load(json_data)
    allLikes = 0
    allComments = 0
    averageLikes = 0
    averageComments = 0    
    number_of_posts = 0
    number_of_users = 0    
    usernameList = []
    for post in posts:
        allLikes += int(post["like_count"])
        allComments += int(post["comment_count"])
        number_of_posts += 1
        if post["username"] not in usernameList:
            number_of_users += 1
            usernameList.append(post["username"])                   
    averageLikes = allLikes/number_of_posts
    averageComments = allComments/number_of_posts    
    averageNumberOfpostsPerUser = number_of_posts/number_of_users
    results = {"Number of posts":number_of_posts, "Number of users":number_of_users,
    "Average number of posts per user":averageNumberOfpostsPerUser,
    "All likes":allLikes,"Average likes":averageLikes,
    "All comments":allComments,"Average comments":averageComments}   
    print("Number of posts: ", number_of_posts)
    print("Number of users: ", number_of_users)
    print("Average number of posts per user: ", averageNumberOfpostsPerUser)
    print("All likes: ", allLikes)
    print("Average likes: ", averageLikes)
    print("All comments: ", allComments)
    print("Average comments: ", averageComments)
    return results

def countNumberOfInfluencers(inputfile):
    occasionalInf = 0
    influencer = 0
    commonUser = 0
    with open(inputfile) as json_data:
      users = json.load(json_data)
    for user in users:
        if user["influence_level"] == 0:
            commonUser += 1
        if user["influence_level"] == 1:
            occasionalInf += 1
        if user["influence_level"] == 2:
            influencer +=1 
    print("Common user: ", commonUser)    
    print("Occasional Influencer: ", commonUser)    
    print("Influencer: ", influencer)

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