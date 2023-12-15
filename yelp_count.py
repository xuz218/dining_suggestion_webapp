import requests

api_key = 'cIOTS7utRsAWbw7DkgkEpE87YUCfDl9AbxedbbcTaK-nlu116jyjUcODTgef8swlG_Dn3F-uCwm3Ht_dVv44yWW_gSaouh8ITwyNo57lHAmmt8EaPJ-YpC0mxfQqZXYx'
search_url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': f'Bearer {api_key}'}

def count_restaurants(location, radius=1000, limit=50):
    offset = 0
    total_count = 0
    while True:
        search_params = {
            'term': 'restaurants',
            'location': location,
            'radius': radius,
            'limit': limit,
            'offset': offset
        }

        response = requests.get(search_url, headers=headers, params=search_params)
        if response.status_code != 200:
            break

        data = response.json()
        total_count += len(data['businesses'])
        if offset + limit >= data['total']:
            break
        offset += limit

    return total_count

restaurant_count = count_restaurants('Columbia University, NYC')
print(f"Restaurant sum: {restaurant_count}")
