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

		
cursor.execute("CREATE USER 'WeatherUser'@'%' IDENTIFIED BY 'WeatherPassword'")
cursor.execute('GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON Weather.* TO 'WeatherUser'@'%'")
#cursor.execute("GRANT ALL ON DjangoFiddle.* TO 'Django'@'%'")

		
#cursor.execute("DROP TABLE `django_content_type`")

#If we get this far, we are game on..
TABLES = {}
TABLES['observations'] = (
    "CREATE TABLE `observations` ("
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


cnx.commit()

#print NObs


