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
    'limit': 1
}

search_response = requests.get(search_url, headers=headers, params=search_params)
search_data = search_response.json()

def printMenu(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    menu_items = soup.find_all('div', class_='dishWrapper__09f24__Bj2sT')

    for item in menu_items:
        name = item.find('p', class_='css-nyjpex').text.strip() if item.find('p', class_='css-nyjpex') else 'No Name'
        price = item.find('span', class_='price__09f24__F1T0p').text.strip() if item.find('span', class_='price__09f24__F1T0p') else 'No Price'
        image = item.find('img', class_='dishImageV2__09f24__VT6Je')
        image_url = image['src'] if image else 'No Image'

        print(f'Dish: {name}, Price: {price}, Image URL: {image_url}')


for business in search_data['businesses']:
    details_url = f"https://api.yelp.com/v3/businesses/{business['id']}"
    details_response = requests.get(details_url, headers=headers)
    details_data = details_response.json()
    website_url = details_data.get('url', '无官网链接')
    print(f"Name: {business['name']}")
    print(f"Address: {', '.join(business['location']['display_address'])}")
    print(f"Score: {business['rating']}")
    print(f"Review_count: {business['review_count']}")
    print(f"Website: {website_url}")
    printMenu(website_url)
    print("---")
