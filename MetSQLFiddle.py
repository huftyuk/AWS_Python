#sudo pip install metoffer
import metoffer
import time
import datetime
import urllib
import urllib2
import mysql.connector

import sys
sys.path.append('/home/ubuntu')
import APIKeyManager
MetDataPointAPIKey = APIKeyManager.MetDataPoint
RDSLogin = APIKeyManager.RDSLogin

import os

import pprint

#Login to the database machine
cnx = mysql.connector.connect(**RDSLogin)
cursor = cnx.cursor()

#Initialise Metoffer and get the list of sites available
M = metoffer.MetOffer(MetDataPointAPIKey)
sitelist = M.loc_observations(metoffer.SITELIST)
sites = metoffer.parse_sitelist(sitelist)

add_obs = ("INSERT INTO observations "
 		"(Loc, tObs, TAmbient, pAmbient, rHumidity) "
 		"VALUES (%s, %s, %s, %s, %s)")

for site in sites:
	try:
		#Start by seeing if we can get the data we want.
		x = M.loc_observations(site.ident)
		y = metoffer.parse_val(x)
		bkeepgoing = 1
	except:
		print "Parse val failed for some reason"
		#So don't do anything more with this ste
		bkeepgoing = 0

	if bkeepgoing:
		for data in y.data[-1]:
			print data
		try:
			TAmbient = str(y.data[-1]["Temperature"][0])
			pAmbient = str(y.data[-1]["Pressure"][0])
#			vWind = str(y.data[0]["Wind Speed"][0])
#			TDewPoint = str(y.data[0]["Dew Point"][0])
			rHumidity = str(y.data[-1]["Screen Relative Humidity"][0])
#			NWeather = str(y.data[0]["Weather Type"][0])
#			xVisibility = str(y.data[0]["Visibility"][0])
			#vWindGust = str(y.data[0]["Wind Gust"][0])

		except:
			print "cant parse data"
			pprint.pprint(y.data[0])
			bkeepgoing = 0

	if bkeepgoing:
		try:
			obs_data = (str(site.name),y.data[-1]["timestamp"][0],TAmbient,pAmbient,rHumidity)
			print obs_data
		except:
			print("cant generate string " + site.name)
			bkeepgoing = 0

	if bkeepgoing:
		try:
			cursor.execute(add_obs, obs_data)
			NObs = cursor.lastrowid
			print NObs
			cnx.commit()
		except:
			print("failed tocommit " +  site.name)

cursor.close()
cnx.close()


