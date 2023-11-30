from flask import Flask, send_from_directory, request, render_template, g, redirect, Response, abort, url_for, session, app
from flask_login import logout_user
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

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

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/profile')
def profile():
    return send_from_directory(app.static_folder, 'profile.html')

@app.route('/rating')
def rating():
    return send_from_directory(app.static_folder, 'rating.html')

@app.route('/search')
def search():
    return send_from_directory(app.static_folder, 'search.html')

@app.route('/signup')
def signup():
    return send_from_directory(app.static_folder, 'signup.html')

if __name__ == '__main__':
    app.run(debug=True)
