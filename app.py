from flask import Flask, send_from_directory, request, render_template, g, redirect, Response, abort, url_for, session, app
# from flask_login import logout_user
import os
import boto3
import json
import requests
# from boto3.dynamodb.conditions import Key, Attr

# app = Flask(__name__, static_folder='front-end')
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__)
app.secret_key = "secretkey"


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def save_user_to_dynamodb(user_data):
    table = dynamodb.Table('User')
    try:
        response = table.put_item(Item=user_data)
        return response
    except Exception as e:
        print(f"Error saving user: {str(e)}")
        return None

dining_halls = {
    'John Jay Dining Hall': {
        'image_url': 'https://magazine.columbia.edu/sites/default/files/styles/wysiwyg_full_width_image/public/2018-11/Campus-dining.jpg?itok=JjmPPX_6',
        'seating_capacity': 'Red',
        'operating_status': 'Operating',
        'rating': '4.6'
    },
    'JJs Place': {
        'image_url': 'https://arc-anglerfish-arc2-prod-spectator.s3.amazonaws.com/public/QSLKMLFR4FANXD7KRYYI5J2BBM',
        'seating_capacity': 'Green',
        'operating_status': 'Closed',
        'rating': '4.2'
    },
    'Ferris Booth Commons': {
        'image_url': 'https://bwog.com/wp-content/uploads/2018/03/dining-97_web_0.jpg',
        'seating_capacity': 'Yellow',
        'operating_status': 'Operating',
        'rating': '4.8'
    }
}

user_info = {
    'name': 'abc',
    'email': 'abc@columbia.edu',
    'user id': '123'
}

@app.route('/')
def index():
    return render_template('index.html', dining_halls=dining_halls)

@app.route('/dining-halls/<hall_name>', methods=['GET'])
def dining_hall_details(hall_name):
    # Replace 'API_ENDPOINT' with the actual API endpoint you are using
    # Assume the API URL structure includes the hall name
    hall_name = hall_name.replace(" ", "")
    api_url = f"https://nx9q5bjiy4.execute-api.us-east-1.amazonaws.com/test/dining-halls/{hall_name}"
    headers = {
        "X-Api-Key": "S6CWXVooge19g3YkToivwa7jHEnqZD188iJGg25R",
        'Access-Control-Allow-Origin': '*',
    }
    response = requests.get(api_url, headers=headers)
                
    if response.status_code == 200:
        menu_data = response.json()
        new_stations = {}
        for menu in menu_data:
            for date_range_field in menu['date_range_fields']:
                for station in date_range_field['stations']:
                    station_id = station['station'][0]
                    if station_id not in new_stations:
                        new_stations[station_id] = {
                            'station': station_id,
                            'meals': []
                        }
                    new_stations[station_id]['meals'].extend(station['meals_paragraph'])

        for station_data in new_stations.values():
            unique_meals = []
            seen_titles = set()
            for meal in station_data['meals']:
                if meal['title'] not in seen_titles:
                    unique_meals.append(meal)
                    seen_titles.add(meal['title'])
            station_data['meals'] = unique_meals
        
        return render_template('dining_hall_details.html', name=hall_name, menus=new_stations)
    else:
        return "Dining hall not found or menu data unavailable", 404

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', user_info = user_info)

@app.route('/restaurant/<rest_name>')
def restDetail(rest_name):
    # Replace 'API_ENDPOINT' with the actual API endpoint you are using
    # Assume the API URL structure includes the hall name
    api_url = f"https://nx9q5bjiy4.execute-api.us-east-1.amazonaws.com/test/restaurant/{rest_name}"
    headers = {
        "X-Api-Key": "S6CWXVooge19g3YkToivwa7jHEnqZD188iJGg25R",
        'Access-Control-Allow-Origin': '*',
    }
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        rest_info = response.json()
        if 'image' not in rest_info or rest_info['image']=="":
                rest_info['image'] = "https://i.pinimg.com/736x/2c/50/20/2c50208241b85db01cc8b2d7a4dc8b22.jpg"
        return render_template('restaurant.html', rest_info=rest_info)
    else:
        return "Restaurant not found or menu data unavailable", 404

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')  # Get the search query from URL parameters
    url = "https://nx9q5bjiy4.execute-api.us-east-1.amazonaws.com/test/recommendsearch/"
    headers = {
        "X-Api-Key": "S6CWXVooge19g3YkToivwa7jHEnqZD188iJGg25R",
        'Access-Control-Allow-Origin': '*',
    }
    params = {
        "q": query
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        tmp = response.json()
        restaurants = json.loads(tmp['body'])['top_five_restaurants']
        top_five_restaurants = restaurants[:]  # Get the top 5 restaurants
            
        for restaurant in top_five_restaurants:
            if 'image' not in restaurant or restaurant['image']=="":
                restaurant['image'] = "https://i.pinimg.com/736x/2c/50/20/2c50208241b85db01cc8b2d7a4dc8b22.jpg"
        
        return render_template('search.html', top_five_restaurants=top_five_restaurants, q=query)
    else:
        # If response is not successful
        return "Internal Server Error", 500

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
