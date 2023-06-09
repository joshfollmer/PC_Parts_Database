import mysql.connector
import configparser as cf
from pcpartpicker import API
import itertools

def connectToDB():
    config = cf.ConfigParser()
    config.read('config.ini')

    db_host = config.get('Database', 'HOST') 
    db_user = config.get('Database', 'USER')
    db_password = config.get('Database', 'PASSWORD')
    db_name = config.get('Database', 'DATABASE')


    conn = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        database = db_name
    )

    return conn.cursor()


api = API()
cpu_data = api.retrieve("cpu")


values = cpu_data.values()
#
flattened_values = itertools.chain(*values)

#relevant attributes: base_clock, boost_clock, brand, cores, integrated graphics, model, multithreading, price, tdp
for element in flattened_values:
    print(element)
    

    
