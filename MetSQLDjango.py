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
RDSLogin = APIKeyManager.RDSDjangoLogin

import os

import pprint

#Login to the database machine
cnx = mysql.connector.connect(**RDSLogin)
cursor = cnx.cursor()

#Initialise Metoffer and get the list of sites available
M = metoffer.MetOffer(MetDataPointAPIKey)
ObservationsList = M.loc_observations(metoffer.CAPABILITIES)
for Observation in ObservationsList["Resource"]["TimeSteps"]["TS"]:
#	print Observation
#	try:
	if 1:
		x = M.loc_observations(metoffer.ALL)
		#publishtime = x["SiteRep"]["DV"]["dataDate"]
		publishtime = datetime.datetime.strptime(x["SiteRep"]["DV"]["dataDate"],"%Y-%m-%dT%H:%M:%SZ")
		observationtime = datetime.datetime.strptime(Observation,"%Y-%m-%dT%H:%M:%SZ")	
		entrytime = datetime.datetime.now()
		print observationtime
#		print publishtime
		#Now see if this is a new observation, or one we've seen before.
		query = ("SELECT NObs FROM polls_observations WHERE timestamp = %s")
		cursor.execute(query,(observationtime,))
		NMatch = 0
		for (NObs) in cursor:
			NMatch += 1
		if NMatch == 0:
			print("Adding records for current time stamp")
			bContinue = 1
		else:
			print ("Not duplicating current time stamp")
			bContinue = 0
#	except:
#		print "Cant get observations"
#		bContinue = 0
	
	if bContinue:
		x2 = x
		for Location in x["SiteRep"]["DV"]["Location"]:
			try:
				a = str(Location["name"])
			except:
				Location["name"] = "Somewhere odd"
			x2["SiteRep"]["DV"]["Location"] = Location
#			try:
			if 1:
				y = metoffer.parse_val(x2)
				fieldnamestring = "(LocationID" 
				formatstring = "VALUES (%s"
				obsdata_list = [Location["i"]]
#				obsdata_list.append(publishtime)
#				obsdata_list.append(entrytime)
#				print y.data[0]
				for data in y.data[0]:
#					print data
					dataname = data
					dataname = data.replace(" ", "_")
					fieldnamestring = fieldnamestring + ", " + dataname
					formatstring = formatstring + ", %s" 
					obsdata_list.append(y.data[0][data][0])
						
				addobs_string = ("INSERT INTO polls_observations " + fieldnamestring + ") " + formatstring + ")" )
				cursor.execute(addobs_string, tuple(obsdata_list))
				NObs = cursor.lastrowid
#			except:
#				print("Something went wrong somewhere, skipping " + Location["name"])
		#Commit everything at this time stamp.
		cnx.commit()
cursor.close()
cnx.close()


