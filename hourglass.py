# importing utility libraries
from urllib.parse import urlencode
import urllib.request
import urllib, json, os, logging, time, random
#Interact w Hue
import requests

# MQTT Client functions
import paho.mqtt.client as mqtt

# getting the current time from python datetime object
from datetime import datetime
from datetime import timedelta

# IP Address of Philips Hue "Sieg Master" Bridge
sieg_master_ip = "172.28.219.179"
#sieg_master_ip = "10.0.1.16"

# API Token we have generated for Sieg Master Bridge
sieg_master_token = "rARKEpLebwXuW01cNVvQbnDEkd2bd56Nj-hpTETB"
#sieg_master_token = "efzstVYGsi1LQDdNF2N4GoR4pSBjCPOpGOX-qK1e"

# light_palette_dict: Contains the values for each light to set all the lights to defined palettes
# Contains the palettes that were already included in the hourglass sketch
# To access: light_palette_dict[lightNum][n]
# n = 0 : "sunset colors"
# n = 1 : "warmer colors"
# Set lights to palette n:
# for lightNum in light_palette_dict:
#     changeLight(lightNum, 2, "hue", light_palette_dict[lightNum][n*3],
#       "bri", light_palette_dict[lightNum][n*3+1], "sat", light_palette_dict[lightNum][n*3+2]);

# Easily add more palettes by adding more values to arrays
# Only for upstairs lights rn
light_palette_dict = {
    #Lightnum: [pallette1Hue,palette1Bri,palette1Sat, [pallette2Hue,palette2Bri,palette2Sat]
    5: [65000,200,100, 45500,200,100],
    8: [8000,254,200, 39500,254,130],
    9: [65000,254,150, 55500254,90],
    12: [8000,254,200, 39500,254,130],
    13: [65000,254,150, 55500254,90],
    17: [63000,200,170, 64400,200,90],
    18: [12345,254,80, 34000,254,100],
    19: [65000,200,100, 45500,200,100],
    20: [10000,254,160, 34900,254,80],
    24: [65000,254,100, 45500,254,100],
    25: [10000,254,160, 34900,254,80],
    26: [8000,254,200, 9500,254,130]
}


# setup: Run once at the beginning
def setup():

    # MQTT Client Setup
    global client
    client = mqtt.Client("csadgsdagsdagsdg")  # create new instance
    client.on_connect = on_connect
    #                      broker_address = "broker.mqttdashboard.com"
    broker_address = "test.mosquitto.org"
    client.connect(broker_address)  # connect to broker
    client.loop_start()
    client.on_message = on_message
    client._keepalive = 60
    #client.publish("hcdeiol/testing", "Hourglass Turned on")  # publish


    #Time Functions Setup
    # Get current time
    current_time = datetime.utcnow()
    # converting current time to 12-hour format for API use
    current_time = current_time.strftime("%I:%M:%S")
    timeurl = sunsetriseREST()
    jsontime = json.load(timeurl)
    print(pretty(jsontime))
    print("Sunset: " + sunset(jsontime))

    # Example to change to palette 1
    # paletteNum = 1
    # for lightNum in light_palette_dict:
    #     changeLight(lightNum, 2, "hue", light_palette_dict[lightNum][paletteNum * 3],
    #                 "bri", light_palette_dict[lightNum][(paletteNum*3)+1], "sat", light_palette_dict[lightNum][(paletteNum*3)+2])


# loop: Run continuously
def loop():
    #changeLight(3, 2, "hue", "10000")
    #time.sleep(10)
    # getting current time in UTC format for sunset-sunrise API use
    current_time = datetime.now()
    #print(current_time)


# MQTT: The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iol")

# MQTT: Message Received Callback
# Checks if the message is JSON formatted data containing the key
# "Lights" or "Groups". If so, parse the JSON and make changes to Philips Hue lighting
def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received: " +m_decode)
    m_in=json.loads(m_decode)
    #print(type(m_in))
    print(pretty(m_in))
    print(m_in.keys())
    if 'Lights' in m_in.keys():
        print("FOUND LIGHTS")
        for indiv_light_dict in m_in['Lights']:
            print(indiv_light_dict.keys())
            for k in indiv_light_dict.keys():
                print("Key: " + k)
                print(indiv_light_dict[k][0].keys())
                on = indiv_light_dict[k][0]["on"]
                hue = indiv_light_dict[k][0]["hue"]
                sat = indiv_light_dict[k][0]["sat"]
                bri = indiv_light_dict[k][0]["bri"]
                #changeLight(k, 2, "on", '"' + on + '"', "hue", '"' + hue + '"', "sat", '"' + sat + '"', "bri", '"' + bri + '"')
                changeLight(k, 2, "on", on , "hue", hue , "sat", sat, "bri", bri)


    if 'Groups' in m_in.keys():
        print("FOUND GROUPS")
        for group_light_dict in m_in['Groups']:
            print(group_light_dict.keys())
            for k in group_light_dict.keys():
                print("Key: " + k)
                print(group_light_dict[k][0].keys())
                on = group_light_dict[k][0]["on"]
                print(on)
                if(on=="true"):
                    print("pushing full group change")
                    hue = group_light_dict[k][0]["hue"]
                    sat = group_light_dict[k][0]["sat"]
                    bri = group_light_dict[k][0]["bri"]
                    changeGroup(k, 2, "on", on, "hue", hue, "sat", sat, "bri", bri)
                    print("pushed")
                else:
                    changeGroup(k, 2, "on", on)
                #changeGroup(k, 2, "on", '"' + on + '"', "hue", '"' + hue + '"', "sat", '"' + sat + '"', "bri", '"' + bri + '"')
                #changeGroup(k, 2, "on", on, "hue", hue, "sat", sat, "bri", bri)

# changeLight: Modify up to 4 parameters of a single light
# Parameter 1: lightNum - see mapping of Sieg lights: https://files.slack.com/files-tmb/TH0QLFCH3-FJGHX7K4P-6ecab43eeb/image_from_ios_720.jpg
# Paramter 2: Transitiontime (1/10ths of a second)
# Paramters 3 - 10: Names and values for Philiphs Hue Lighting paramters
# Example usage: changeLight(21,2,"on","true","hue", "30000")
# Turns light 21 to a greenish color

def changeLight(lightNum, transitiontime, parameter1, newValue1, parameter2=None, newValue2=None, parameter3=None,
                newValue3=None, parameter4=None, newValue4=None):
    req_string = "http://" + str(sieg_master_ip) + "/api/" + str(sieg_master_token) + "/lights/" + str(
        lightNum) + "/state";
    print("change light")
    put_string = "{\"" + str(parameter1) + "\":" + str(newValue1) + ", \"transitiontime\":" + str(transitiontime);
    if (parameter2 != None):
        put_string += ", \"" + parameter2 + "\": " + newValue2;
    if (parameter3 != None):
        put_string += ", \"" + parameter3 + "\" : " + newValue3;
    if (parameter4 != None):
        put_string += ", \"" + parameter4 + "\" : " + newValue4;
    put_string += "}";

    print(req_string + "  " + put_string)
    r = requests.put(req_string, put_string, verify=True)
    print(r)


# changeGroup: Modify up to 4 parameters of a group of lights
# Parameter 1: groupNum - group 0 is all lights, group 1 is bottom floor, group 2 is top floor
# Paramter 2: Transitiontime (1/10ths of a second)
# Paramters 3 - 10: Names and values for Philiphs Hue Lighting paramters
# Example usage: changeGroup(1,2,"on","true","hue", "10000", "bri", "254")
# Turns bottom floor to a bright white
def changeGroup(groupNum, transitiontime, parameter1, newValue1, parameter2=None, newValue2=None, parameter3=None,
                newValue3=None, parameter4=None, newValue4=None):
    req_string = "http://" + str(sieg_master_ip) + "/api/" + str(sieg_master_token) + "/groups/" + str(
        groupNum) + "/action";
    put_string = "{\"" + str(parameter1) + "\":" + str(newValue1) + ", \"transitiontime\":" + str(transitiontime);
    if (parameter2 != None):
        put_string += ", \"" + parameter2 + "\": " + newValue2;
    if (parameter3 != None):
        put_string += ", \"" + parameter3 + "\" : " + newValue3;
    if (parameter4 != None):
        put_string += ", \"" + parameter4 + "\" : " + newValue4;
    put_string += "}";
    print(req_string + "  " + put_string)
    r = requests.put(req_string, put_string, verify=True)
    print(r)

# Return a readable version of json data for print debugging
def pretty(obj):  # help to read the json format easier to read
    return json.dumps(obj, sort_keys=True, indent=2)


# Return results of a urlopen request, handling errors
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




# --------------------- getting sunset and sunrise time with comparison to the current time in UTC format -------------------------#
# setting up the API at University of Washington latitude and longtitude
def sunsetriseREST():
    params = {'lat': 47.655548, 'lng': -122.303200} #UW Lat/Long
    baseurl = 'https://api.sunrise-sunset.org/json?'
    # params['lat'] = 47.655548  # UW Latitude
    # params['lng'] = -122.303200  # UW Longitude

    url = baseurl + urlencode(params)
    return safeGet(url)


# getting the sunrise time at Seattle/UW in UTC format
def sunrise(dict):
    sunrisetime = json.load['results']['sunrise']
    # getting sunrise time without AM/PM char
    sunrisetime = sunrisetime[:8]
    return sunrisetime


# getting the sunset time at Seattle/UW in UTC format
def sunset(dict):
    sunsettime = dict['results']['sunset']
    # getting sunset time without AM/PM char
    sunsettime = sunsettime
    #datetime_object = datetime.strptime
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


# Use a "main" function to run all code. Use a "while True" loop within main to repeat code
if __name__ == "__main__":
    # Run Once
    setup()
    # Initialize loop
    while True:
        loop()



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
