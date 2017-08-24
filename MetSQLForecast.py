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

#for site in sites:
#site = sites[1]
#	print site.name
#	try:
	#Start by seeing if we can get the data we want.
#xtest = M.loc_forecast(sites[0].ident,metoffer.THREE_HOURLY)
#pprint.pprint(xtest["SiteRep"]["DV"]["Location"])

x = M.loc_forecast(metoffer.ALL,metoffer.THREE_HOURLY)
#pprint.pprint(x["SiteRep"]["DV"]["Location"][0])

#	print x.keys()
for Location in x["SiteRep"]["DV"]["Location"]:
	x2 = x
	x2["SiteRep"]["DV"]["Location"] = Location
#	pprint.pprint(x["SiteRep"])
	pprint.pprint(x2)
	y = metoffer.parse_val(x2)
	bkeepgoing = 1
#	except:
#		print "Parse val failed for some reason"
#		#So don't do anything more with this ste
#		bkeepgoing = 0

	if bkeepgoing:
		fieldnamestring = "(Location, PublishTime" 
		formatstring = "VALUES (%s, %s"
		obsdata_list = [str(Location["name"])]
		publishtime = y.data_date
		print publishtime
		print y.data[-1]["timestamp"][0]
		publushtime = datetime.datetime.strptime(publishtime,"%Y-%m-%dT%H:%M:%SZ")
		obsdata_list.append(publushtime)
#		pprint.pprint(y.data)
		for data in y.data[-1]:
			dataname = data
			dataname = data.replace(" ", "_")
#			print dataname
			fieldnamestring = fieldnamestring + ", " + dataname
			formatstring = formatstring + ", %s" 
			obsdata_list.append(y.data[-1][data][0])
			
		addobs_string = ("INSERT INTO forecasts " + fieldnamestring + ") " + formatstring + ")" )

#		print addobs_string
#		print add_obs
#		print tuple(obsdata_list)

#Now see if this is a new observation, or one we've seen before.
		query = ("SELECT NObs FROM forecasts WHERE Location = %s AND PublishTime = %s")
		cursor.execute(query,(str(Location["name"]),publushtime))

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
			print ("Not duplicating" +  (str(Location["name"]))
cursor.close()
cnx.close()


