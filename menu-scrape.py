from bs4 import BeautifulSoup
import requests

url = 'https://www.yelp.com/biz/the-ellington-new-york-4?adjust_creative=OBuAiqMaM0UOarnKVXeohA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=OBuAiqMaM0UOarnKVXeohA'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

# 根据您提供的结构，我们假设每个菜单项都包含在 'dishWrapper__09f24__Bj2sT' 类的 div 中
menu_items = soup.find_all('div', class_='dishWrapper__09f24__Bj2sT')

for item in menu_items:
    # 提取菜品名称
    name = item.find('p', class_='css-nyjpex').text.strip() if item.find('p', class_='css-nyjpex') else 'No Name'

    # 提取价格
    price = item.find('span', class_='price__09f24__F1T0p').text.strip() if item.find('span', class_='price__09f24__F1T0p') else 'No Price'

    # 提取图片链接
    image = item.find('img', class_='dishImageV2__09f24__VT6Je')
    image_url = image['src'] if image else 'No Image'

    print(f'Name: {name}, Price: {price}, Image URL: {image_url}')
