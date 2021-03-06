import mysql.connector
import datetime
import sys
sys.path.append('/home/ubuntu')
import APIKeyManager
from mysql.connector import errorcode


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

RDSLogin = APIKeyManager.RDSLogin
cnx = mysql.connector.connect(**RDSLogin)
cursor = cnx.cursor()


DB_NAME = 'Weather'

try:
    cnx.database = DB_NAME 
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

		
#cursor.execute("CREATE USER 'WeatherUser'@'%' IDENTIFIED BY 'Secret'")
#cursor.execute('GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON Weather.* TO 'WeatherUser'@'%'")
#cursor.execute("GRANT ALL ON Weather.* TO 'WeatherUser'@'%'")

		
cursor.execute("DROP TABLE `forecasts`")

#If we get this far, we are game on..
TABLES = {}
TABLES['observations'] = (
    "CREATE TABLE `observations` ("
    " `NObs` int NOT NULL AUTO_INCREMENT,"
    " `timestamp` datetime NOT NULL,"
    " `LocationID` mediumint NOT NULL,"
    " `Temperature` float,"
    " `Pressure` mediumint,"
    " `Screen_Relative_Humidity` float,"
    " `Wind_Speed` tinyint,"
    " `Visibility` int,"
    " `Dew_Point` float,"
    " `Pressure_Tendency` varchar(5),"
    " `Weather_Type` tinyint,"
    " `Wind_Direction` char(3),"
    " `Wind_Gust` tinyint,"
    " PRIMARY KEY (`NObs`)"
    ") ENGINE=InnoDB")

#TABLES = {}
TABLES['forecasts'] = (
    "CREATE TABLE `forecasts` ("
    " `NObs` int NOT NULL AUTO_INCREMENT,"
    " `timestamp` datetime NOT NULL,"
    " `PublishTime` datetime NOT NULL,"
    " `EntryTime` datetime NOT NULL,"
    " `LocationID` mediumint NOT NULL,"
    " `Temperature` tinyint,"
    " `Feels_Like_Temperature` tinyint,"
    " `Screen_Relative_Humidity` tinyint,"
    " `Wind_Speed` tinyint,"
    " `Visibility` char(4),"
    " `Dew_Point` tinyint,"
    " `Weather_Type` tinyint,"
    " `Wind_Direction` char(3),"
    " `Max_UV_Index` tinyint,"
    " `Precipitation_Probability` tinyint,"
    " `Wind_Gust` smallint,"
    " PRIMARY KEY (`NObs`)"
    ") ENGINE=InnoDB")

#    " `Pressure_Tendency` varchar(5),"
#    " `Pressure` smallint,"
	
for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ".format(name))
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


cnx.commit()

#print NObs


