import requests
from bs4 import BeautifulSoup

api_key = 'cIOTS7utRsAWbw7DkgkEpE87YUCfDl9AbxedbbcTaK-nlu116jyjUcODTgef8swlG_Dn3F-uCwm3Ht_dVv44yWW_gSaouh8ITwyNo57lHAmmt8EaPJ-YpC0mxfQqZXYx'
search_url = 'https://api.yelp.com/v3/businesses/search'

headers = {
    'Authorization': 'Bearer %s' % api_key,
}

search_params = {
    'term': 'restaurants',
    'location': 'Columbia University, NYC',
    'radius': 1609,
    'limit': 20
}

search_response = requests.get(search_url, headers=headers, params=search_params)
search_data = search_response.json()

def printMenu(url):
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


for business in search_data['businesses']:
    details_url = f"https://api.yelp.com/v3/businesses/{business['id']}"
    details_response = requests.get(details_url, headers=headers)
    details_data = details_response.json()
    website_url = details_data.get('url', '无官网链接')
    print(f"餐馆名称: {business['name']}")
    print(f"地址: {', '.join(business['location']['display_address'])}")
    print(f"评分: {business['rating']}")
    print(f"评论数: {business['review_count']}")
    print(f"官网链接: {website_url}")
    printMenu(website_url)
    print("---")
