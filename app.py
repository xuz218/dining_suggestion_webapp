from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='front-end')

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
