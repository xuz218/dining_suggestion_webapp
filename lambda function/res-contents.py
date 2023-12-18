import json
import pymysql
import os
import csv

# Retrieve database credentials from environment variables
DB_HOST = 'diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'xxxxx'
DB_NAME = 'diningdb'

def lambda_handler(event, context):
    connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                             
    rest_name = event['pathParameters']['rest-name']
    if not rest_name:
        return {'statusCode': 404, 'body': 'Restaurant not found'}

    rest_name = rest_name.replace("%20", " ")
    
    with connection.cursor() as cursor:
        cursor.execute("""
            select name, rating, menu, image_url, ROUND(average, 2) AS average
            from restaurant
            where restaurant.name = %s
        """, (rest_name))
    
        rest_info = cursor.fetchall()
        
        cursor.execute("""
            SELECT
                c.comment,
                DATE_FORMAT(c.timestamp, '%%Y-%%m-%%d %%H:%%i:%%s') as timestamp,
                u.email
            FROM
                comment c
            JOIN
                restaurant r ON c.restaurant_id = r.restaurant_id
            JOIN
                user u ON c.user_id = u.user_id
            WHERE
                r.name = %s
        """, (rest_name))
    
        comments = cursor.fetchall()
        
    connection.commit()
    connection.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'success',
            'rest_info': rest_info,
            'comments': comments
        })
    }
