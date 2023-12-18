import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

hall_name_to_url = {
    'JohnJayDiningHall': 'https://dining.columbia.edu/content/john-jay-dining-hall',
    'JJsPlace': 'https://dining.columbia.edu/content/jjs-place-0',
    'FerrisBoothCommons': 'https://dining.columbia.edu/content/ferris-booth-commons-0'
}

    
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')

    table_name = 'diningHall'
    print(event)
    print(context)
    # return {
    #     'statusCode': 200,
    #     'body': 'hello'
    # }

    # Assume hall_name is passed as a path parameter in the event
    hall_name = event['pathParameters']['hall-name']
    

    url = hall_name_to_url.get(hall_name)
    print(hall_name)
    print(url)

    if not url:
        return {'statusCode': 404, 'body': 'Dining hall not found'}

    table = dynamodb.Table(table_name)

    try:
        response = table.scan(FilterExpression=Attr('url').eq(url))
        # print(response)
        if 'Items' in response:
            print(response['Items'][-1])
            closest_menu_item = response['Items'][-1]['menu_data']
            # print(closest_menu_item)
            return {
                'statusCode': 200,
                'body': json.dumps(closest_menu_item)
            }
        else:
            # Item not found
            return {
                'statusCode': 404,
                'body': 'Item not found'
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Error retrieving item'
        }
