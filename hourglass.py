# HOURGLASS:

# importing utility libraries
from urllib.parse import urlencode
import urllib.request
import urllib, json, os, logging, time, random

# getting the current time from python datetime object
from datetime import datetime




sieg_master_ip = "172.28.219.179"

sieg_master_token = "rARKEpLebwXuW01cNVvQbnDEkd2bd56Nj-hpTETB"

#changeLight: Modify up to 4 parameters of a single light
#Parameter 1: lightNum - see mapping of Sieg lights: https://files.slack.com/files-tmb/TH0QLFCH3-FJGHX7K4P-6ecab43eeb/image_from_ios_720.jpg
#Paramter 2: Transitiontime (1/10ths of a second)
#Paramters 3 - 10: Names and values for Philiphs Hue Lighting paramters
#Example usage: changeLight(21,2,"on","true","hue", "30000")
#Turns light 21 to a greenish color

def changeLight(lightNum, transitiontime, parameter1, newValue1, parameter2 = None, newValue2 = None, parameter3 = None,
                newValue3 = None, parameter4 = None, newValue4 = None):

    req_string = "http://" + str(sieg_master_ip) + "/api/" + str(sieg_master_token) + "/lights/" + str(lightNum) + "/state";

    put_string = "{\"" + str(parameter1) + "\":" + str(newValue1) + ", \"transitiontime\":" + str(transitiontime);
    if (parameter2 != None):
        put_string +=  ", \"" + parameter2 + "\": " + newValue2;
    if (parameter3 != None):
        put_string += ", \"" + parameter3 + "\" : " + newValue3;
    if (parameter4 != None):
        put_string += ", \"" + parameter4 + "\" : " + newValue4;
    put_string += "}";
    requests.put(req_string, put_string, verify=True)


#changeGroup: Modify up to 4 parameters of a group of lights
#Parameter 1: groupNum - group 0 is all lights, group 1 is bottom floor, group 2 is top floor
#Paramter 2: Transitiontime (1/10ths of a second)
#Paramters 3 - 10: Names and values for Philiphs Hue Lighting paramters
#Example usage: changeGroup(1,2,"on","true","hue", "10000", "bri", "254")
#Turns bottom floor to a bright white
def changeGroup(groupNum, transitiontime, parameter1, newValue1, parameter2 = None, newValue2 = None, parameter3 = None,
                newValue3 = None, parameter4 = None, newValue4 = None):

    req_string = "http://" + str(sieg_master_ip) + "/api/" + str(sieg_master_token) + "/groups/" + str(groupNum) + "/action";

    put_string = "{\"" + str(parameter1) + "\":" + str(newValue1) + ", \"transitiontime\":" + str(transitiontime);
    if (parameter2 != None):
        put_string +=  ", \"" + parameter2 + "\": " + newValue2;
    if (parameter3 != None):
        put_string += ", \"" + parameter3 + "\" : " + newValue3;
    if (parameter4 != None):
        put_string += ", \"" + parameter4 + "\" : " + newValue4;
    put_string += "}";
    requests.put(req_string, put_string, verify=True)

#Return a readable version of json data for print debugging
def pretty(obj):  # help to read the json format easier to read
    return json.dumps(obj, sort_keys=True, indent=2)


#HReturn results of a urlopen request, handling errors
def safeGet(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print("Error code: ", e.code)
    except urllib.URLError as e:
        print("We failed to reach a server")
        print("Reason: ", e.reason)
    return None


# getting the json format API
def dict(url):
    jsondict = json.load(url)
    return jsondict


# --------------------- getting sunset and sunrise time with comparison to the current time in UTC format -------------------------#
# setting up the API at University of Washington latitude and longtitude
def sunsetriseREST():
    params = {'lat': 47.655548, 'lng' : -122.303200}
    baseurl = 'https://api.sunrise-sunset.org/json?'
    #params['lat'] = 47.655548  # UW Latitude
    #params['lng'] = -122.303200  # UW Longitude

    url = baseurl + urlencode(params) #PYTHON 3 (might work with 2)
    return safeGet(url)

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



# getting sunrise time from API in UTC format
def sunriseFunction(dict):
    rise = sunrise(dict)
    if (rise == current_time):
        print('yay')


# getting sunset time from API in UTC format
def sunsetFunction(dict):
    set = sunset(dict)
    if set == current_time:
        print("Mamma we made it")
        # some HUE light effects???


#Use a "main" function to run all code. Use a "while True" loop within main to repeat code
def main():
    # Run Once
    thisdict = {
        5: [65000, 45500],
        8: [8000, 39500],
        9: [65000, 55500]
        12: [8000, 39500],
        13: [8000, 39500],
        17: [8000, 39500],
        18: [8000, 39500],
        19: [8000, 39500],
        20: [8000, 39500],
        24: [8000, 39500],
        25: [8000, 39500],
        26: [8000, 39500]
    }
    #Get current time
    current_time = datetime.utcnow()
    # converting current time to 12-hour format for API use
    current_time = current_time.strftime("%I:%M:%S")
    timeurl = sunsetriseREST()
    jsontime = dict(timeurl)
    print(pretty(jsontime))

    # Iterating over keys
    for lightNum in thisdict:
        print(thisdict[lightNum][0])

    # Initialize loop
    while True:
        print("S")
        time.sleep(10)
        # getting current time in UTC format for sunset-sunrise API use
        #current_time = datetime.utcnow()
        #print(current_time)

main()


# -------------------- working to get US holidays ---------------------------#
# using holiday API from https://holidayapi.pl/

def holidayREST():
    baseurl = ''



# UPPER LOBBY LIGHTS
# ---------sunset colors-----------------#
# light <id>    "hue",  "bri",  "sat"
#       5       65000   200     100
#       8       8000    254     200
#       9       65000   254     150
#       12      8000    254     200
#       13      65000   254     150
#       17      63000   200     170
#       18      12345   254     80
#       19      65000   200     100
#       20      10000   254     160
#       24      65000   254     100
#       25      10000   254     160
#       26      8000    254     200

# ------------------------------------------#
# ------------colder palette----------------#
# light <id>    "hue",  "bri",  "sat"
#       5       45500   200     100
#       8       39500   254     130
#       9       55500   254     90
#       12      39500   254     130
#       13      55500   254     90
#       17      64400   200     90
#       18      34000   254     100
#       19      45500   200     100
#       20      34900   254     80
#       24      45500   254     100
#       25      34900   254     80
#       26      39500   254     130
# -----------------------------------------#
