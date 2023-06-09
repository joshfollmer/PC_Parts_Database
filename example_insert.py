import mysql.connector
import configparser as cf

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

cursor = conn.cursor()
sql = "INSERT INTO Example (evalue) VALUES (%s)"

values = (10,)
cursor.execute(sql, values)

conn.commit()

cursor.close()
conn.close()
import configparser as cf

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

cursor = conn.cursor()
sql = "INSERT INTO Example (evalue) VALUES (%s)"

values = (10,)
cursor.execute(sql, values)

conn.commit()

cursor.close()
conn.close()