#Code to call the MySQL Database
import os
import mysql.connector
from dotenv import load_dotenv

#Load env variables
load_dotenv()
def sql_connect():
    health_db = mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        database= os.getenv("DB_NAME"),
    ) 

    return health_db  

#Create a callable connection
