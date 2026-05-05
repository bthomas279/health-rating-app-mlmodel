#Code to call the MySQL Database
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

#Load env variables
load_dotenv()

def sql_connect():
    """Function to connect to the database
        """
    try:
        health_db = mysql.connector.connect(
            host= os.getenv("DB_HOST"),
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            database= os.getenv("DB_NAME"),
        ) 

    #Catch connection error
    except Error as e:
        print(f"Error found while connecting to database. Error:", {e})

    return health_db 



#Class for database
class Database_Connections():
    """Contains all the functions for the database calls"""




    def __init__(self, user_id, request):
        """"""

        self.user_id = user_id
        self.request = request 

    #Create a callable connection
    def sql_call(self):
        """Function to call the database based on what the user wants to grab.

        Attributes:
            command: I don't remember why this is here

        Returns:
            some sort of json file of their information
        """
        cursor = sql_connect().cursor()

        #if they request for regRate
        if self.request == "regRate":
            query = f"SELECT app_user_id, reg_mental_health_rating, created_at FROM mental_health_scores WHERE app_user_id = {self.user_id}"
        
        #if they request for classRate
        if self.request == "classRate":
            query = f"SELECT app_user_id, class_mental_health_rating, created_at FROM mental_health_scores WHERE app_user_id = {self.user_id}"

        #if they request for study hours
        if self.request == "study_hours":
            query = f"SELECT user_id, study_hours, created_at FROM user_habits WHERE user_id = {self.user_id}"

        #if they request for sleep_hours
        if self.request == "sleep_hours":
            query = f"SELECT user_id, study_hours, created_at FROM user_habits WHERE user_id = {self.user_id}"

        #Execute query
        cursor.execute(query)
        
        #Return Response
        response = cursor.fetchmany(10)
        print(response) #REMOVE LATER!!!
        return response