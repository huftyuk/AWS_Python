#pip install datapoint
#https://github.com/jacobtomlinson/datapoint-python
import datapoint  
import sys
sys.path.append('/home/ubuntu')
import APIKeyManager

apikey = APIKeyManager.MetDataPoint


# Create datapoint connection
conn = datapoint.Manager(api_key=apikey)

# Get nearest site and print out its name
site = conn.get_nearest_site(-0.124626, 51.500728)
print site.name

# Get a forecast for the nearest site
forecast = conn.get_forecast_for_site(site.id, "3hourly")

# Get the current timestep using now() and print out some info
now = forecast.now()
print now.weather.text
print "%s%s%s" % (now.temperature.value,
                  u'\xb0', #Unicode character for degree symbol
                  now.temperature.units)
