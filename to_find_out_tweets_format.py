from __future__ import absolute_import, print_function
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import tweepy
from tweepy.utils import import_simplejson
import string


def log_msg(filepath, text, date):
    with open(filepath, "a") as myfile:
        myfile.write(date + "\n" + str(text.encode('utf-8')) + "\n-------------------------\n")


def remove_unprintable(text):
    text = filter(lambda x: x in string.printable, text)
    return text


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        # print(data)
        json_tweet = json.loads(data)
        if "text" in json_tweet:
            text = remove_unprintable(json_tweet["text"])
            date = json_tweet["created_at"]
            log_msg("output.txt", text, date)


if __name__ == '__main__':
    l = StdOutListener()

    consumer_key = "Es3lDZ9L6ukHRUl1ya5uOTPtx"
    consumer_secret = "4UmLc6z65P9Z7nveZnBKssKEnPV71svogCwvhnKaIvM44syi5B"
    access_token = "370737927-rr0xbO21qRS92QgCLqvU9qg1FDqic6vuWTlncT0x"
    access_token_secret = "ql8fXdZ4acRTDNAi4aZHq1OefpIz6qt8eTXQdj0s79IWK"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['basketball', 'GSOPAO', '#GSOPAO', 'panathinaikos'])