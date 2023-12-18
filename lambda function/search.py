import json
import pymysql
import os
import csv

# Retrieve database credentials from environment variables
DB_HOST = 'diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'xxxxx'
DB_NAME = 'diningdb'

def searchdb(category_label=None, uid=None):
    connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        if category_label != None and uid != None:
            print('1')
            cursor.execute("""
                SELECT 
                    r.name, 
                    r.rating, 
                    r.address, 
                    r.image_url, 
                    r.category, 
                    r.menu, 
                    r.average, 
                    COALESCE(i.is_favorite, 0) as is_favorite
                FROM 
                    restaurant r
                LEFT JOIN 
                    (SELECT * FROM interactions WHERE user_id = %s) i ON r.restaurant_id = i.restaurant_id
                WHERE 
                    r.category LIKE %s
                ORDER BY 
                    r.rating DESC
                LIMIT 15
            """, (uid, '%'+category_label+'%'))

        elif uid != None:
            print('2')
            cursor.execute("""
                SELECT 
                    r.name, 
                    r.rating, 
                    r.address, 
                    r.image_url, 
                    r.category, 
                    r.menu, 
                    r.average, 
                    COALESCE(i.is_favorite, 0) as is_favorite
                FROM 
                    restaurant r
                LEFT JOIN 
                    (SELECT * FROM interactions WHERE user_id = %s) i ON r.restaurant_id = i.restaurant_id
                ORDER BY 
                    r.rating DESC
                LIMIT 15
            """, (uid))
        else:
            
            print('3')
            cursor.execute("""
                SELECT 
                    r.name, 
                    r.rating, 
                    r.address, 
                    r.image_url, 
                    r.category, 
                    r.menu, 
                    r.average, 
                    0
                FROM 
                    restaurant r
                ORDER BY 
                    r.rating DESC
                LIMIT 15
            """)
        
        # cursor.execute("desc restaurant")
        result = cursor.fetchall()
        # result = json.dumps(result)
        
    connection.commit()
    connection.close()

    return result

def lambda_handler(event, context):
    label = event['queryStringParameters'].get('q', 'No query provided').lower()
    sort = event['queryStringParameters'].get('sort', 'No sort').lower()
    uid = event['queryStringParameters'].get('uid', 'No user id').lower()
    
    print(event)
    print("start searching")
    
    if label == '' and uid == '':
        matching_restaurants = searchdb()
    elif uid == '':
        matching_restaurants = searchdb(label)
    else:
        matching_restaurants = searchdb(label, uid)
        
    # print(event)
    # print(query)
    # print(sort)
    
    matching_restaurants = sorted(matching_restaurants, key=lambda x: x['name'])
    if sort == 'rating':    
        matching_restaurants = sorted(matching_restaurants, key=lambda x: x['rating'], reverse=True)
    elif sort == 'price-asc':
        matching_restaurants = sorted(matching_restaurants, key=lambda x: x['average'], reverse=True)
    elif sort == 'price-desc':
        matching_restaurants = sorted(matching_restaurants, key=lambda x: x['average'], reverse=False)
        
    
    response = {
        'statusCode': 200,
        'body': json.dumps({
            # 'message': f"Hello, I am the lambda! I received your query: {query}, {sort}",
            'resulted_restaurants': matching_restaurants
        })
    }
    return response