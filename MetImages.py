#sudo pip install metoffer
import metoffer
import time
import datetime
import urllib
import urllib2
import mysql.connector
import json

import sys
sys.path.append('/home/ubuntu')
import APIKeyManager
MetDataPointAPIKey = APIKeyManager.MetDataPoint
RDSLogin = APIKeyManager.RDSWeatherLogin

import os

import pprint


#Initialise Metoffer and get the list of sites available
M = metoffer.MetOffer(MetDataPointAPIKey)
ImageList = M.stand_alone_imagery()
pprint.pprint(ImageList)

#ForceastOverlayList = M.map_overlay_forecast()
#ObservationOverlayList = map_overlay_obs()