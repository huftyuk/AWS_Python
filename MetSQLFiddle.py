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

cnx = mysql.connector.connect(**RDSLogin)
cursor = cnx.cursor()

M = metoffer.MetOffer(MetDataPointAPIKey)

sitelist = M.loc_observations(metoffer.SITELIST)
sites = metoffer.parse_sitelist(sitelist)

for site in sites:
	NObsFailures = 0	
	NTSFailures = 0	
	#We will split the process into 2 things.
	#The first is getting the weather data, the second one is sending it to TS.
	x = M.loc_observations(site.ident)
	try:
		y = metoffer.parse_val(x)
		bkeepgoing = 1
	except:
		print " parse val failed"
		bkeepgoing = 0

	if bkeepgoing:
		try:
			TAmbient = str(y.data[-1]["Temperature"][0])
			pAmbient = str(y.data[-1]["Pressure"][0])
#			vWind = str(y.data[0]["Wind Speed"][0])
#			TDewPoint = str(y.data[0]["Dew Point"][0])
			rHumidity = str(y.data[-1]["Screen Relative Humidity"][0])
#			NWeather = str(y.data[0]["Weather Type"][0])
#			xVisibility = str(y.data[0]["Visibility"][0])

		except:
			print "cant parse data"
			pprint.pprint(y.data[0])
			bkeepgoing = 0
		add_obs = ("INSERT INTO observations "
 				"(Loc, tObs, TAmbient, pAmbient, rHumidity) "
 				"VALUES (%s, %s, %s, %s, %s)")

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
			print("failed toncommit " +  site.name)


			#vWindGust = str(y.data[0]["Wind Gust"][0])
			#pprint.pprint(y.data)
#			urlstring = TSbaseURL  + "&field1=" + TAmbient + "&field2=" + pAmbient + "&field3=" + vWind + "&field4=" + TDewPoint + "&field5=" + rHumidity + "&field6=" + NWeather + "&field7=" + xVisibility
#			print urlstring
#			print("Temperature is " + str(y.data[0]["Temperature"][0]))
#			lasttime = y.data_date
		bSendToTS = 0
#		except:
#			time.sleep(30)
#			NTSFailures = NTSFailures + 1
#			if NTSFailures == 10:
#				urllib2.urlopen('https://maker.ifttt.com/trigger/tsreboot/with/key/fF_oXNFLzvmF_Rlpn1_NDiabvQobeCYJ_QVfX39DqbV')
#				os.system('sudo reboot')
				#reboot

#	time.sleep(2)
	bNeedNewObs = 1
	bLoop =0

cursor.close()
cnx.close()


