#sudo pip install metoffer
import metoffer
import time
import datetime
import urllib
import urllib2
6
import sys
sys.path.append('/home/ubuntu')
import APIKeyManager
MetDataPointAPIKey = APIKeyManager.MetDataPoint
import os

import pprint

location = sys.argv[1]
print location
if location == 'Guildford':
	TSbaseURL = 'https://api.thingspeak.com/update?api_key=W1SUNO795Y0QXY0E'   #Guildford
	Lat = 51.4033
	Long = -0.3375
elif location == "Rotherham":
	TSbaseURL = 'https://api.thingspeak.com/update?api_key=W03HJ322D3OFBEG8'   #Rotherham
	Lat = 53.4083859
	Long = -1.3472005
M = metoffer.MetOffer(MetDataPointAPIKey)
#x = M.nearest_loc_forecast(-0.5935112, 51.2339491, metoffer.THREE_HOURLY)

lasttime = datetime.datetime.now()
print lasttime

bNeedNewObs = 1
bSendToTS = 1


while 1:
	NObsFailures = 0	
	NTSFailures = 0	
	#We will split the process into 2 things.
	#The first is getting the weather data, the second one is sending it to TS.
	while bNeedNewObs:
		try:
			#Get some observations
			x = M.nearest_loc_obs(Lat, Long)
			y = metoffer.parse_val(x)
			bNeedNewObs = 0
		except:
			time.sleep(20)
			NObsFailures = NObsFailures + 1
			if NObsFailures == 10:
				urllib2.urlopen('https://maker.ifttt.com/trigger/metreboot/with/key/fF_oXNFLzvmF_Rlpn1_NDiabvQobeCYJ_QVfX39DqbV')
				os.system('sudo reboot')
				#Reboot
		
	print(y.data_date)	
	if lasttime == y.data_date:
		print "No new data, keep going"
		bSendToTS = 0
	else:
		bSendToTS = 1
		
	while bSendToTS:
		try:
			TAmbient = str(y.data[0]["Temperature"][0])
			pAmbient = str(y.data[0]["Pressure"][0])
			vWind = str(y.data[0]["Wind Speed"][0])
			TDewPoint = str(y.data[0]["Dew Point"][0])
			rHumidity = str(y.data[0]["Screen Relative Humidity"][0])
			NWeather = str(y.data[0]["Weather Type"][0])
			xVisibility = str(y.data[0]["Visibility"][0])
			#vWindGust = str(y.data[0]["Wind Gust"][0])
			#pprint.pprint(y.data)
			urlstring = TSbaseURL  + "&field1=" + TAmbient + "&field2=" + pAmbient + "&field3=" + vWind + "&field4=" + TDewPoint + "&field5=" + rHumidity + "&field6=" + NWeather + "&field7=" + xVisibility
			print urlstring
			#f = urllib.urlopen(urlstring)
			#print f.read()
			dweeturlstring = "https://dweet.io/dweet/for/huftysweather?"  + "TAmbient=" + TAmbient + "&pAmbient=" + pAmbient + "&vWind=" + vWind + "&TDewPoint=" + TDewPoint + "&rHumidity=" + rHumidity + "&NWeather=" + NWeather + "&xVisibility=" + xVisibility
			f = urllib.urlopen(dweeturlstring)
			print("Temperature is " + str(y.data[0]["Temperature"][0]))
			lasttime = y.data_date	
			bSendToTS = 0
		except:
			time.sleep(30)
			NTSFailures = NTSFailures + 1
			if NTSFailures == 10:
				urllib2.urlopen('https://maker.ifttt.com/trigger/tsreboot/with/key/fF_oXNFLzvmF_Rlpn1_NDiabvQobeCYJ_QVfX39DqbV')
				os.system('sudo reboot')
				#reboot
			
	time.sleep(20)
	bNeedNewObs = 1
