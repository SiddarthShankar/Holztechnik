import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Siddarth#1011',
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE Holztechnik")

print("Created Dpatabase")