#This code provides a wrapper function for work done by Connor to send put requests
#to the Philips Hue web API.

#Functions:
#       changeLight - send up to 4 param changes to 1 light
#       changeGroup - send up to 4 param changes to a group of lights

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sieg_master_ip = "172.28.219.179"

sieg_master_token = "rARKEpLebwXuW01cNVvQbnDEkd2bd56Nj-hpTETB"

#changeLight: Modify up to 4 parameters of a single light
#Parameter 1: lightNum - see mapping of Sieg lights: https://files.slack.com/files-tmb/TH0QLFCH3-FJGHX7K4P-6ecab43eeb/image_from_ios_720.jpg
#Parameter 2: Transitiontime (1/10ths of a second)
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
#Parameter 2: Transitiontime (1/10ths of a second)
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

#changeGroup(1,2,"on","true","hue", "10000", "bri", "254")