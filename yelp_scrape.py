import requests

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

for business in search_data['businesses']:
    print(f"餐馆名称: {business['name']}")
    print(f"地址: {', '.join(business['location']['display_address'])}")
    print(f"评分: {business['rating']}")
    print(f"评论数: {business['review_count']}")
    details_url = f"https://api.yelp.com/v3/businesses/{business['id']}"
    details_response = requests.get(details_url, headers=headers)
    details_data = details_response.json()
    print(details_data)
    image_url = details_data.get('image_url', '无图片')
    print(f"图片链接: {image_url}")
    print("---")
