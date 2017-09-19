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
#print ImageList.keys
#pprint.pprint(ImageList)
for Chart in ImageList["BWSurfacePressureChartList"]["BWSurfacePressureChart"]:
	URI = Chart["ProductURI"]
	URI = URI.replace("{key}",MetDataPointAPIKey)
	print URI
ForecastOverlayList = M.map_overlay_forecast()
#pprint.pprint(ForecastOverlayList["Layers"])
BaseURL = ForecastOverlayList["Layers"]["BaseUrl"]["$"]
BaseURL = BaseURL.replace("{key}",MetDataPointAPIKey)

print BaseURL
for Layer in ForecastOverlayList["Layers"]["Layer"]:
	print Layer["@displayName"]
	LayerURL = BaseURL.replace({"{LayerName}",Layer["Service"]["LayerName"]
	print LayerURL
	for TimeStep i  Layer["Service"]["TimeSteps"]["Timestep"]:
		print TimeStep
		URL = BaseURL.replace(
	#pprint.pprint(Layer)
	
#ObservationOverlayList = map_overlay_obs()
