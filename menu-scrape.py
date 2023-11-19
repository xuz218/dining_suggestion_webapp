from bs4 import BeautifulSoup
import requests

url = 'https://www.yelp.com/biz/the-ellington-new-york-4?adjust_creative=OBuAiqMaM0UOarnKVXeohA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=OBuAiqMaM0UOarnKVXeohA'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

menu_items = soup.find_all('div', class_='dishWrapper__09f24__Bj2sT')

for item in menu_items:
    name = item.find('p', class_='css-nyjpex').text.strip() if item.find('p', class_='css-nyjpex') else 'No Name'
    price = item.find('span', class_='price__09f24__F1T0p').text.strip() if item.find('span', class_='price__09f24__F1T0p') else 'No Price'

    image = item.find('img', class_='dishImageV2__09f24__VT6Je')
    image_url = image['src'] if image else 'No Image'

    print(f'Name: {name}, Price: {price}, Image URL: {image_url}')
