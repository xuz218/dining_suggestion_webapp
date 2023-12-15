import requests
from bs4 import BeautifulSoup
import csv

api_key = 'cIOTS7utRsAWbw7DkgkEpE87YUCfDl9AbxedbbcTaK-nlu116jyjUcODTgef8swlG_Dn3F-uCwm3Ht_dVv44yWW_gSaouh8ITwyNo57lHAmmt8EaPJ-YpC0mxfQqZXYx'
headers = {'Authorization': f'Bearer {api_key}'}
base_url = 'https://api.yelp.com/v3/businesses/search'

limit = 50
offset = 0
total = None

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

def write_to_csv(filename, data):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

csv_filename = 'restaurant_data.csv'
headers = ['yelp_id', 'name', 'category', 'image', 'address', 'rating', 'review_count', 'menu']
write_to_csv(csv_filename, [headers])

while total is None or offset < total:
    search_params = {
        'term': 'restaurants',
        'location': 'Columbia University, NYC',
        'radius': 1609,
        'limit': limit,
        'offset': offset
    }

    response = requests.get(base_url, headers=headers, params=search_params)
    data = response.json()
    total = data['total']
    businesses = data.get('businesses', [])

    for business in businesses:
        # 与原始代码相同，处理每个业务
        # ...

        # 准备写入CSV的数据
        row = [
            business_id,
            business.get('name', ''),
            ', '.join([category.get('alias', '') for category in business.get('categories', [])]),
            business.get('image_url', ''),
            ', '.join(business.get('location', {}).get('display_address', [])),
            str(business.get('rating', 0)),
            str(business.get('review_count', 0)),
            str(menu_items)
        ]

        # 写入CSV
        write_to_csv(csv_filename, [row])

    offset += limit
