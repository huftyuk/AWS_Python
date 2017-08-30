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

RDSLogin = APIKeyManager.RDSWeatherLogin
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

#cursor.execute("CREATE USER 'Django'@'%' IDENTIFIED BY 'DjangoPass'")
#cursor.execute('GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON DjangoFiddle.* TO 'Django'@'%'")
#cursor.execute("GRANT ALL ON DjangoFiddle.* TO 'Django'@'%'")



#cursor.execute("DROP TABLE `django_content_type`")

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

TABLES = {}
	
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




#Code to insert into a table
add_obs = ("INSERT INTO observations "
              "(tObs, Loc, TAmbient, pAmbient, rHumidity) "
              "VALUES (%s, %s, %s, %s, %s)")

obs_data = (datetime.datetime.now(), 'Guildford', 10, 1000,  80)
#cursor.execute(add_obs, obs_data)
#NObs = cursor.lastrowid
cnx.commit()


#Example of some queries
#query = ("SELECT NObs,Loc,tObs,TAmbient FROM observations WHERE tObs BETWEEN %s AND %s")
#obs_start = datetime.datetime(2017, 8, 8,01,01,01)
#obs_end = datetime.datetime(2017, 8, 18,18,01,01)
#query = ("SELECT NObs,Loc,tObs,TAmbient FROM observations WHERE tObs BETWEEN %s AND %s")
#cursor.execute(query, (obs_start, obs_end))

#And another
#query = ("SELECT timestamp, Temperature FROM observations2" " WHERE Location = 'Coningsby'")
#cursor.execute(query)

#nmatch = 0
#for (timestamp, Temperature) in cursor:
#  nmatch += 1
#  print("{}, {}".format(
#    timestamp,Temperature))

#print nmatch

#And another
query = ("SELECT timestamp, Temperature FROM observations" " WHERE LocationID = 14")
cursor.execute(query)

nmatch = 0
for (timestamp, Temperature) in cursor:
  nmatch += 1
  print("{}, {}".format(
    timestamp,Temperature))

print nmatch




cursor.close()
cnx.close()
