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
    with connection.cursor() as cursor:
            uid = json.loads(event['body'])['uid']
            name = json.loads(event['body'])['name']
            email = json.loads(event['body'])['email']
            cursor.execute("""insert into user(user_id, name, username, email, health_goal, weekly_budget)
            values(%s, %s, %s, %s, "Maintain Health", 400.0)""", (uid, name, name, email))
            res = cursor.fetchall()
            connection.commit()
    connection.close()
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({
            'message': "success",
        })
    }
