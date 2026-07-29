import os
import mysql.connector
from mysql.connector import Error

# Khai báo db_config gom chung
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),          
    'password': os.getenv('DB_PASSWORD', '123456'),          
    'database': os.getenv('DB_NAME', 'hethongcv') 
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
        return None