import urllib, urllib2, webbrowser, json

import os
import logging

#getting the current time from python datetime object
from datetime import datetime
import time

#getting current time in UTC format for sunset-sunrise API use
current_time = datetime.utcnow()

#converting current time to 12-hour format for API use
current_time = current_time.strftime("%I:%M:%S")

print (current_time)


####below are methods working with API####

def pretty(obj): #help to read the json format easier
    return json.dumps(obj, sort_keys=True, indent=2)

#getting the API Url in a safer way
def safeGet(url):
    try:
        return urllib.urlopen(url)
    except urllib2.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib2.error.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None

#setting up the API at University of Washington latitude and longtitude
def sunsetriseREST(params={}):
    baseurl = 'https://api.sunrise-sunset.org/json?'
    params['lat'] = 47.655548
    params['lng'] = -122.303200

    url = baseurl + urllib.urlencode(params)
    return safeGet(url)

#getting the json format API
def timedict(url):
    jsondict = json.load(url)
    return jsondict

timeurl = sunsetriseREST()
jsontime = timedict(timeurl)
print (pretty(jsontime))

#getting the sunrise time at Seattle/UW in UTC format
def sunrise(dict):
    sunrisetime = dict['results']['sunrise']
    #getting sunrise time without AM/PM char
    sunrisetime - sunrisetime[:7]
    return sunrisetime

#getting the sunset time at Seattle/UW in UTC format
def sunset(dict):
    sunsettime = dict['results']['sunset']
    #getting sunset time without AM/PM char
    sunsettime = sunsettime[:7]
    return sunsettime

print sunset(jsontime)

#def timeToSunrise(dict):
#    rise = sunrise(dict)
#    if(rise == current_time) {
#    #some HUE light effects???
#    }

#def timeToSunset(dict):
#    set = sunset(dict)
#    if(set == current_time) {
#    #some HUE light effects???
#    }

