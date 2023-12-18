import json
import pymysql
import os
import csv

# Retrieve database credentials from environment variables
DB_HOST = 'diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'xxxxx'
DB_NAME = 'diningdb'

# Database connection

def lambda_handler(event, context):
    uid = json.loads(event['body'])['q']
    res_name = json.loads(event['body'])['res']
    status = json.loads(event['body'])['status']
    
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    with connection.cursor() as cursor:
        new_status = 1 if status == False else 0
        
        cursor.execute("select restaurant_id from restaurant where restaurant.name = %s", (res_name))
        restaurant_id = cursor.fetchone()['restaurant_id']

        cursor.execute("""
            SELECT COUNT(*)
            FROM interactions
            WHERE user_id = %s AND restaurant_id = %s
        """, (uid, restaurant_id))
        result = cursor.fetchone()
        print(result)
        
        # If there's no existing interaction, result will be (0,)
        if result['COUNT(*)']==0:
            cursor.execute("""
                INSERT INTO interactions (user_id, restaurant_id, is_favorite)
                VALUES (%s, %s, 1)
            """, (uid, restaurant_id))
        else:
            cursor.execute("""
                UPDATE interactions
                SET is_favorite = %s
                WHERE user_id = %s AND restaurant_id = %s
            """, (new_status, uid, restaurant_id))
        connection.commit()
    
    # Make sure to close the connection
    connection.close()
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': "success"
    }
