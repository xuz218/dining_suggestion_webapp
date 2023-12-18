import json
import pymysql
import os
import csv

# Retrieve database credentials from environment variables
DB_HOST = 'diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'xxxxxxx'
DB_NAME = 'diningdb'

# Database connection

def lambda_handler(event, context):
    print(event)
    userid = event['queryStringParameters'].get('q', 'No query provided').lower()
    print(userid)
    connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:

        # cursor.execute('''insert into user(user_id, health_goal, weekly_budget, email, username, name)
        # values ('bd68ee1f-d97d-4f6d-a719-a5154fc057b9', 'Maintain Health', 400.0, 'zhangyizhenyizen@gmail.com', 'Yizhen', 'Zhang, Yizhen')''')
        
        cursor.execute("""SELECT user_id, name, username, email, health_goal, weekly_budget
        from user
        where user.user_id = %s""", (userid))
        result1 = cursor.fetchall()
        print(result1)
        
        cursor.execute("""
            SELECT
                r.name,
                r.image_url,
                r.rating,
                r.address
            FROM
                interactions i
            JOIN
                restaurant r ON i.restaurant_id = r.restaurant_id
            WHERE
                i.is_favorite = 1
                AND i.user_id = %s
            """, (userid))
        result2 = cursor.fetchall()
        
    connection.commit()
    connection.close()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'user_info': result1,
            'saved_restaurants': result2
        })
    }
