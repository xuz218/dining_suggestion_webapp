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

@app.route('/dining-hall/<hall_name>')
def dining_hall_details(hall_name):
    # Replace 'API_ENDPOINT' with the actual API endpoint you are using
    # Assume the API URL structure includes the hall name
    api_url = f"https://nx9q5bjiy4.execute-api.us-east-1.amazonaws.com/test/dining-hall/{hall_name}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        menu_data = response.json()
        return render_template('dining_hall_details.html', name=hall_name, menu=menu_data)
    else:
        return "Dining hall not found or menu data unavailable", 404

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', user_info = user_info)

@app.route('/rating')
def rating():
    return render_template('rating.html')

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
        top_five_restaurants = restaurants[:5]  # Get the top 5 restaurants
            
        for restaurant in top_five_restaurants:
            if 'image' not in restaurant:
                restaurant['image'] = "https://i.pinimg.com/736x/2c/50/20/2c50208241b85db01cc8b2d7a4dc8b22.jpg"
        
        return render_template('search.html', top_five_restaurants=top_five_restaurants)
    else:
        # If response is not successful
        return "Internal Server Error", 500

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
