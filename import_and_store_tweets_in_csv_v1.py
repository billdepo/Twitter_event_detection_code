#!/usr/bin/python
# -*- coding: utf-8 -*-
from tweepy import Stream #tweepy library enables Python to communicate with Twitter platform and use its API
from tweepy import OAuthHandler #OAuth = open authentication and authorisation - used for handling our twitter details
from tweepy.streaming import StreamListener #StreamListener enables to receive tweets
import csv
import json

#consumer key, consumer secret, access token, access secret.
ckey = "Es3lDZ9L6ukHRUl1ya5uOTPtx"
csecret = "4UmLc6z65P9Z7nveZnBKssKEnPV71svogCwvhnKaIvM44syi5B"
atoken = "370737927-rr0xbO21qRS92QgCLqvU9qg1FDqic6vuWTlncT0x"
asecret = "ql8fXdZ4acRTDNAi4aZHq1OefpIz6qt8eTXQdj0s79IWK"

savefile = open('file.tsv', 'w', encoding='utf-8') #opening (creating when not present) a new file "file.tsv" for saving the csv files (tweets) and creating an object named savefile
#'w' mode: Opens a file for writing only. Overwrites the file if the file exists. If the file does not exist, creates a new file for writing.
savefile.write("User\tTweet\n") #writing the headers in the file (please note that we use tab-deliminated text file)
savefile.close() #closing the file    ------ JUST A NOTE HERE - it may be better to use the "with" command for file openning

#creating a stramlistener - In Tweepy, an instance of tweepy.Stream establishes a streaming session and routes messages to StreamListener instance.
class listener(StreamListener):

    def on_data(self, data): #method of a stream listener that receives all messages and calls functions according to the message type - Called when raw data is received from connection

        tweet_dict = json.loads(data) # transforms string to dictionary
        try: # we use the exception utility because of the occasional tweet that fails in the stream
            username = tweet_dict["user"]["screen_name"]  # store tweet's user - it is in the dict screen_name which lies within the dict user
            tweet = tweet_dict["text"]  # store tweet's text
            tweet = tweet.replace('\n', '')  # removes all newline characters from tweet's text
            print((username, tweet)) #print the tweet to the console

            savefile = open('file.tsv', 'a', encoding='utf8')  #'a' – Appending mode, which is used to add new data to the end of the file
            savefile.write("%s\t%s\n" % (username, tweet)) #writing the tsv file with the selected tweet's data in tab-deliminated format
            savefile.close() #closing the file ----- again we could use "with" command

        except KeyError:
            pass    #if an error occurs (can happen e.g. with encoding problems) just pass and do nothing so the execution of the program doesn't stop


        # Open, write and close your file.
        #savefile = csv.writer(open('file.csv', 'a', encoding='utf8'))
        #savefile.writerows([[username, tweet]])
        #savefile = open('file.txt', 'a', encoding='utf8')

    #def on_status(self, status):


        #sheet = csv.writer(open('file.csv', 'a', encoding='utf8'))
        #sheet.writerow([status.author.screen_name, status.created_at, status.text])

        #with open('file.csv', 'a', encoding='utf8') as f:
        #    writer = csv.writer(f)
        #    writer.writerow([status.text])


    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret) #providing authorisation for streaming twitter
auth.set_access_token(atoken, asecret) #setting the access tokens

twitterStream = Stream(auth, listener()) #tweepy Stream class -- first argument authorisation credentials - second argument the StreamListener class we have defined
twitterStream.filter(languages=['en'], track=['trump', 'nba'])