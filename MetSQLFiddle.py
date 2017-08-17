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
#site = sites[1]

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
		fieldnamestring = "(Location" 
		formatstring = "VALUES (%s"
		obsdata_list = [str(site.name)]
		
		for data in y.data[-1]:
			dataname = data
			dataname = data.replace(" ", "_")
#			print dataname
			fieldnamestring = fieldnamestring + ", " + dataname
			formatstring = formatstring + ", %s" 
			obsdata_list.append(y.data[-1][data][0])
			
		addobs_string = ("INSERT INTO observations2 " + fieldnamestring + ") " + formatstring + ")" )

#		print addobs_string
#		print add_obs
#		print tuple(obsdata_list)

#Now see if this is a new observation, or one we've seen before.
	query = ("SELECT NObs FROM observations2 WHERE Location = " + str(site.name) + " AND timestamp = " + y.data[-1][data][0])
	cursor.execute(query)

	nmatch = 0
	for (NObs) in cursor:
		nmatch += 1
	print nMatch
	if nMatch > 0:
		cursor.execute(addobs_string, tuple(obsdata_list))
		NObs = cursor.lastrowid
		print(str(NObs) + str(site.name))
		cnx.commit()
		
cursor.close()
cnx.close()


