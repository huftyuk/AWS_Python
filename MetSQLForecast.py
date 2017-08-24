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
sitelist = M.loc_forecast(metoffer.SITELIST,metoffer.THREE_HOURLY)
sites = metoffer.parse_sitelist(sitelist)

add_obs = ("INSERT INTO forecast "
 		"(Loc, tObs, TAmbient, pAmbient, rHumidity) "
 		"VALUES (%s, %s, %s, %s, %s)")

x = M.loc_forecast(metoffer.ALL,metoffer.THREE_HOURLY)

for Location in x["SiteRep"]["DV"]["Location"]:
	x2 = x
	try:
		a = str(Location["name"])
	except:
		Location["name"] = "Somewhere odd"
	x2["SiteRep"]["DV"]["Location"] = Location

	try:
		y = metoffer.parse_val(x2)
		fieldnamestring = "(LocationID, PublishTime" 
		formatstring = "VALUES (%s, %s"
		obsdata_list = [Location["i"]]
		publishtime = y.data_date
		publushtime = datetime.datetime.strptime(publishtime,"%Y-%m-%dT%H:%M:%SZ")
		obsdata_list.append(publushtime)
		for data in y.data[-1]:
			dataname = data
			dataname = data.replace(" ", "_")
			fieldnamestring = fieldnamestring + ", " + dataname
			formatstring = formatstring + ", %s" 
			obsdata_list.append(y.data[-1][data][0])
			
		addobs_string = ("INSERT INTO forecasts " + fieldnamestring + ") " + formatstring + ")" )

#Now see if this is a new observation, or one we've seen before.
		query = ("SELECT NObs FROM forecasts WHERE LocationID = %s AND PublishTime = %s")
		cursor.execute(query,(Location["i"],publushtime))

		NMatch = 0
		for (NObs) in cursor:
			NMatch += 1
		print NMatch
		if NMatch == 0:
			cursor.execute(addobs_string, tuple(obsdata_list))
			NObs = cursor.lastrowid
			print("Adding " + str(NObs) + " " + (str(Location["name"])))
			cnx.commit()
		else:
			print ("Not duplicating" +  (str(Location["name"])))
	except:
		print "Something went wrong somewhere, skipping this one"
cursor.close()
cnx.close()


