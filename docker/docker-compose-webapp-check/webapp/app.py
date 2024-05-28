# webapp/app.py
from flask import Flask
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)
@app.route('/')
def check_db_connection():
 try:
    connection = mysql.connector.connect(host='mysql',database='testdb',user='user',password='password')
    if connection.is_connected():
        db_info = connection.get_server_info()
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        return f"Connected to MySQL Server version {db_info}. Connected to database: {record}"
 except Error as e:
        return f"Error while connecting to MySQL: {e}"
 finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
if __name__ == '__main__':
 app.run(host='0.0.0.0')
