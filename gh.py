import urllib, urllib2, webbrowser, json
import os
import logging

# getting the current time from python datetime object
from datetime import datetime
import time

# getting current time in UTC format for sunset-sunrise API use
current_time = datetime.utcnow()

# converting current time to 12-hour format for API use
current_time = current_time.strftime("%I:%M:%S")


# print (current_time)


####below are methods working with API####

def pretty(obj):  # help to read the json format easier to read
    return json.dumps(obj, sort_keys=True, indent=2)


# getting the API Url in a safer way
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

# getting the json format API
def dict(url):
    jsondict = json.load(url)
    return jsondict


#--------------------- getting sunset and sunrise time with comparison to the current time in UTC format -------------------------#
# setting up the API at University of Washington latitude and longtitude
def sunsetriseREST(params={}):
    baseurl = 'https://api.sunrise-sunset.org/json?'
    params['lat'] = 47.655548
    params['lng'] = -122.303200

    url = baseurl + urllib.urlencode(params)
    return safeGet(url)


# test code
# timeurl = sunsetriseREST()
# jsontime = dict(timeurl)
# print (pretty(jsontime))

# getting the sunrise time at Seattle/UW in UTC format
def sunrise(dict):
    sunrisetime = dict['results']['sunrise']
    # getting sunrise time without AM/PM char
    sunrisetime = sunrisetime[:8]
    return sunrisetime


# getting the sunset time at Seattle/UW in UTC format
def sunset(dict):
    sunsettime = dict['results']['sunset']
    # getting sunset time without AM/PM char
    sunsettime = sunsettime[:7]
    return sunsettime


# print sunset(jsontime)

#getting sunrise time from API in UTC format
def timeToSunrise(dict):
    rise = sunrise(dict)
    if(rise == current_time):
        print ('yay')

#getting sunset time from API in UTC format
# def timeToSunset(dict):
#    set = sunset(dict)
#    if(set == current_time) {
#    #some HUE light effects???
#    }

#-------------------- working to get US holidays ---------------------------#
#using holiday API from https://holidayapi.pl/

def holidayREST():
    baseurl = ''


