import json
import pymysql
import os
import csv

# Retrieve database credentials from environment variables
DB_HOST = 'diningdb.ccyvfdlvgzvx.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'xxxxx'
DB_NAME = 'diningdb'

def searchdb_top_rating():
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                r.name, 
                r.rating, 
                r.address, 
                r.image_url, 
                r.category, 
                r.menu, 
                r.average,
                0 as is_favorite
            FROM 
                restaurant r
            ORDER BY 
                r.rating DESC
            LIMIT 10
        """)
        result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result

def searchdb_by_ids(uid, final_restaurant_ids):
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        restaurant_ids_str = ','.join(['%s'] * len(final_restaurant_ids))
        sql_query = """
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
                r.restaurant_id IN ({})
        """.format(restaurant_ids_str)
        parameters = tuple([uid] + final_restaurant_ids)
        cursor.execute(sql_query, parameters)
        result = cursor.fetchall()

    connection.commit()
    connection.close()

    return result
    
def searchfav(user_id):
    connection = pymysql.connect(host=DB_HOST,
                                 user=DB_USER,
                                 password=DB_PASSWORD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                r.restaurant_id
            FROM 
                restaurant r
            LEFT JOIN 
                (SELECT * FROM interactions WHERE user_id = %s) i ON r.restaurant_id = i.restaurant_id
            WHERE
                i.is_favorite = 1
            ORDER BY 
                r.rating DESC
        """, (user_id))
        result = cursor.fetchall()

    connection.commit()
    connection.close()
    
    return result

def lambda_handler(event, context):
    print(event)
    
    body = json.loads(event['body'])
    restaurants = body.get('top_10_items', [])
    restaurant_ids = [item['itemId'] for item in restaurants]
    print('restaurant_ids:', restaurant_ids)
    uid = event['queryStringParameters'].get('uid', '').lower()

    if uid == "none":  
        matching_restaurants = searchdb_top_rating()
    else:
        fav_items = searchfav(uid)
        fav_item_ids = list(set([item['restaurant_id'] for item in fav_items]))
        final_restaurant_ids = fav_item_ids[:3]
        matching_restaurants1 = searchdb_by_ids(uid, final_restaurant_ids)
        for id in restaurant_ids:
            if id not in final_restaurant_ids and len(final_restaurant_ids) < 10:
                final_restaurant_ids.append(id)
        matching_restaurants2 = searchdb_by_ids(uid, final_restaurant_ids[3:])
        matching_restaurants = matching_restaurants1 + matching_restaurants2
    print("matching:", matching_restaurants)
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'resulted_restaurants': matching_restaurants
        })
    }
    return response