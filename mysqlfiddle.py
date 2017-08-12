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


DB_NAME = 'WeatherFiddle'


try:
    cnx.database = DB_NAME 
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

cursor.execute("DROP TABLE `observations2`")

#If we get this far, we are game on..
TABLES = {}
TABLES['observations'] = (
    "CREATE TABLE `observations` ("
    " `NObs` int(11) NOT NULL AUTO_INCREMENT,"
    " `tObs` datetime NOT NULL,"
    " `Loc` varchar(30) NOT NULL,"
    " `TAmbient` float,"
    " `pAmbient` int,"
    " `rHumidity` float,"
    " PRIMARY KEY (`NObs`)"
    ") ENGINE=InnoDB")

TABLES = {}
TABLES['observations2'] = (
    "CREATE TABLE `observations2` ("
    " `NObs` int(11) NOT NULL AUTO_INCREMENT,"
    " `timestamp` datetime NOT NULL,"
    " `Location` varchar(30) NOT NULL,"
    " `Temperature` float,"
    " `Pressure` int,"
    " `Screen_Relative_Humidity` float,"
    " `Wind_Speed` float,"
    " `Visibility` float,"
    " `Dew_Point` float,"
    " `Pressure_Tendency` varchar(5),"
    " `Weather_Type` int,"
    " `Wind_Direction` varchar(4),"
    " `Wind_Gust` float,"
    " PRIMARY KEY (`NObs`)"
    ") ENGINE=InnoDB")

	
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





add_obs = ("INSERT INTO observations "
              "(tObs, Loc, TAmbient, pAmbient, rHumidity) "
              "VALUES (%s, %s, %s, %s, %s)")




obs_data = (datetime.datetime.now(), 'Guildford', 10, 1000,  80)


#cursor.execute(add_obs, obs_data)


#NObs = cursor.lastrowid

cnx.commit()

print NObs




query = ("SELECT NObs,Loc,tObs,TAmbient FROM observations "
         "WHERE tObs BETWEEN %s AND %s")


obs_start = datetime.datetime(2017, 8, 8,01,01,01)
obs_end = datetime.datetime(2017, 8, 18,18,01,01)

cursor.execute(query, (obs_start, obs_end))



print cursor

for (NObs, Loc, tObs,TAmbient) in cursor:
  print("{}, {} at time {} was {}".format(
    NObs, Loc, tObs,TAmbient))

cursor.close()
cnx.close()
