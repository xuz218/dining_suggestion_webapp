import boto3
import requests
from bs4 import BeautifulSoup
import decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurant')

    api_key = 'xxxxx'
    headers = {'Authorization': f'Bearer {api_key}'}
    base_url = 'https://api.yelp.com/v3/businesses/search'

    # Parameters for pagination
    limit = 50
    offset = 0
    total = None

    while total is None or offset < total:
        search_params = {
            'term': 'restaurants',
            'location': 'Columbia University, NYC',
            'radius': 1000,  # One mile in meters
            'limit': limit,
            'offset': offset
        }

        response = requests.get(base_url, headers=headers, params=search_params)
        data = response.json()
        total = data['total']
        businesses = data.get('businesses', [])

        for business in businesses:
            business_id = business['id']
            details_response = requests.get(f'https://api.yelp.com/v3/businesses/{business_id}', headers=headers)
            details = details_response.json()

            menu_items = extract_menu_items(details.get('url', ''))
            rating = decimal.Decimal(str(business.get('rating', 0)))
            review_count = decimal.Decimal(str(business.get('review_count', 0)))
            
            table.put_item(
               Item={
                   'yelp_id': business_id,
                   'name': business.get('name', ''),
                   'image': business.get('image_url', ''), 
                   'address': ', '.join(business.get('location', {}).get('display_address', [])),
                   'rating': rating,
                   'review_count': review_count,
                   'menu': menu_items,
               }
            )
        offset += limit

    return {'statusCode': 200, 'body': 'Data successfully updated in DynamoDB'}

def extract_menu_items(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        menu_items = soup.find_all('div', class_='dishWrapper__09f24__Bj2sT')
        menu = []
        for item in menu_items:
            name = item.find('p', class_='css-nyjpex').text.strip() if item.find('p', class_='css-nyjpex') else 'No Name'
            price = item.find('span', class_='price__09f24__F1T0p').text.strip() if item.find('span', class_='price__09f24__F1T0p') else 'No Price'
            image = item.find('img', class_='dishImageV2__09f24__VT6Je')
            image_url = image['src'] if image else 'No Image'
            menu.append({'name': name, 'price': price, 'image_url': image_url})
        return menu
    except Exception as e:
        print(f"Error extracting menu: {e}")
        return []