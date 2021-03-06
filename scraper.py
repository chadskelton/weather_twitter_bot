#!/usr/bin/env python

# Was getting 502 errors but then changed to Python 2.7.9 runtime (instead of Python 2.7.6). Seemed to grab the page OK then but had some issues with Tweepy

# @WarmerVancouver

import scraperwiki
import tweepy
import time
from datetime import datetime
import smtplib
import requests
from BeautifulSoup import BeautifulSoup
import random
import datetime
import os

TWEEPY_CONSUMER_KEY = os.environ['MORPH_CONSUMER_KEY']
TWEEPY_CONSUMER_SECRET = os.environ['MORPH_CONSUMER_SECRET']
TWEEPY_ACCESS_TOKEN = os.environ['MORPH_ACCESS_TOKEN']
TWEEPY_ACCESS_TOKEN_SECRET = os.environ['MORPH_ACCESS_TOKEN_SECRET']

auth1 = tweepy.auth.OAuthHandler(TWEEPY_CONSUMER_KEY, TWEEPY_CONSUMER_SECRET)
auth1.set_access_token(TWEEPY_ACCESS_TOKEN, TWEEPY_ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth1)
api = tweepy.API(auth1, secure=True)

url = "http://weather.gc.ca/canada_e.html"

html = requests.get(url, verify=False)
htmlpage = html.content

# debugging

print htmlpage

# end debugging

soup = BeautifulSoup(htmlpage)

table = soup.find ("tbody")

rows = table.findAll ("tr")

for row in rows:
    cells = row.findAll ("td")
    city = cells[0].text
    rawdegrees = cells[2].text
    degrees = int(rawdegrees.replace('&deg;C',''))
    if 'Vancouver' in city:
        vancouvertemp = degrees
    # print city
    # print degrees

record = []

recordlist = []

for row in rows:
    cells = row.findAll ("td")
    city = cells[0].text
    rawdegrees = cells[2].text
    degrees = int(rawdegrees.replace('&deg;C',''))
    if degrees < vancouvertemp:
        record = []
        if "Ottawa" in city:
            city = "Ottawa"
        record.append(city)
        record.append(degrees)
        record.append(vancouvertemp - degrees)
        recordlist.append(record)
        
        # record["city"] = city
        # record["degrees"] = degrees
        # record["difference"] = (vancouvertemp-degrees)
        # recordlist.append(record)

print recordlist

choice = random.choice(recordlist)
    
print choice

amount = ""

if choice[2] > 0:
    amount = "a tiny bit"
if choice[2] > 2:
    amount = "a little bit"
if choice[2] > 5:
    amount = "quite a bit"
if choice[2] > 10:
    amount = "a lot"
if choice[2] > 20:
    amount = "waaay"
if choice[2] > 30:
    amount = "ridiculously"
    
statusupdate = "It's " + amount + " warmer in Vancouver right now (" + str(vancouvertemp) + "C) than in " + choice[0] + " (" + str(choice[1]) + "C). "

print statusupdate

api.update_status(status=statusupdate)
