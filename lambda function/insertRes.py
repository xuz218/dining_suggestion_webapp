import json
import pymysql
import os
import csv

# Retrieve database credentials from environment variables
DB_HOST = 'diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'xxxxxx'
DB_NAME = 'diningdb'

# Database connection
connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def lambda_handler(event, context):
    email = event['queryStringParameters'].get('q', 'No query provided').lower()
    restaurant_name = event['queryStringParameters'].get('res', 'No query provided').lower()
    with connection.cursor() as cursor:
        
        cursor.execute("""
            UPDATE interactions i
            JOIN restaurant r ON i.restaurant_id = r.restaurant_id
            SET i.is_favorite = 1
            WHERE i.user_id = %s AND r.name = %s
        """, (user_id, restaurant_name))
    
        result = cursor.fetchall()
        
    connection.commit()
    connection.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'success',
            'result': result
        })
    }
