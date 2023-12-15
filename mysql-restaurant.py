import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host='diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com',  # 替换为你的 RDS Endpoint
        database='diningdb',  # 替换为你的数据库名称
        user='admin',  # 替换为你的数据库用户名
        password='Zhang1998!')  # 替换为你的数据库密码

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
