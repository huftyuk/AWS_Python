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

#Login to the database machine
cnx = mysql.connector.connect(**RDSLogin)
cursor = cnx.cursor()

#Initialise Metoffer and get the list of sites available
M = metoffer.MetOffer(MetDataPointAPIKey)
ForecastList = M.loc_forecast(metoffer.CAPABILITIES,metoffer.THREE_HOURLY)
for Forecast in ForecastList["Resource"]["TimeSteps"]["TS"]:
	print Forecast
	x = M.loc_forecast(metoffer.ALL,metoffer.THREE_HOURLY,Forecast)
	publishtime = x["SiteRep"]["DV"]["dataDate"]
	publushtime = datetime.datetime.strptime(publishtime,"%Y-%m-%dT%H:%M:%SZ")
	forecasttime = datetime.datetime.strptime(Forecast,"%Y-%m-%dT%H:%M:%SZ")	
	print forecasttime
	print publushtime
	#Now see if this is a new observation, or one we've seen before.
	query = ("SELECT NObs FROM forecasts WHERE PublishTime = %s AND timestamp = %s")
	cursor.execute(query,(publushtime,forecasttime))
	NMatch = 0
	for (NObs) in cursor:
		NMatch += 1
	if NMatch == 0:
		print("Adding records for current time stamp")
		bContinue = 1
	else:
		print ("Not duplicating current time stamp")
		bContinue = 0
	
	if bContinue:
		x2 = x
		for Location in x["SiteRep"]["DV"]["Location"]:
	#	x2 = x
			try:
				a = str(Location["name"])
			except:
				Location["name"] = "Somewhere odd"
			x2["SiteRep"]["DV"]["Location"] = Location

			try:
				y = metoffer.parse_val(x2)
			
				if bContinue:
					for forecast in y.data:
						fieldnamestring = "(LocationID, PublishTime" 
						formatstring = "VALUES (%s, %s"
						obsdata_list = [Location["i"]]
						obsdata_list.append(publushtime)
						for data in forecast:
							dataname = data
							dataname = data.replace(" ", "_")
							fieldnamestring = fieldnamestring + ", " + dataname
							formatstring = formatstring + ", %s" 
							obsdata_list.append(forecast[data][0])
						
						addobs_string = ("INSERT INTO forecasts " + fieldnamestring + ") " + formatstring + ")" )
						cursor.execute(addobs_string, tuple(obsdata_list))
						NObs = cursor.lastrowid
			#Commit everything for this location
			#	print Location["i"]
			except:
				print "Something went wrong somewhere, skipping this one"
		cnx.commit()
cursor.close()
cnx.close()


