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

#If we get this far, we are game on..
TABLES = {}
TABLES['observations'] = (
    "CREATE TABLE `observations` ("
    " `NObs` int(11) NOT NULL AUTO_INCREMENT,"
    " `tObs` datetime NOT NULL,"
    " `Loc` varchar(14) NOT NULL,"
    " `TAmbient` int(4) NOT NULL,"
    " `pAmbient` int(4) NOT NULL,"
    " `rHumidity` int(3) NOT NULL,"
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


cursor.execute(add_obs, obs_data)


NObs = cursor.lastrowid

cnx.commit()

print NObs




cursor.close()
cnx.close()
