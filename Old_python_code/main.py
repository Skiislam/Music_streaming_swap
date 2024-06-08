from flask import Flask, redirect, request, jsonify, session
import requests
import urllib.parse
import os 
from datetime import datetime, timedelta
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

user_playlists = {}

@app.route('/')

def index():
    return "Welcome to Spotify app <a href = '/login'> Login with Spotify </a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {
        'client_id' : CLIENT_ID,
        'response_type' : 'code',
        'scope' : scope,
        'redirect_uri' : REDIRECT_URI,
        'show_dialog' : True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})
    if 'code' in request.args:
        req_body = {
            'code' : request.args['code'],
            'grant_type' : 'authorization_code',
            'redirect_uri' : REDIRECT_URI,
            'client_id' : CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlists')
    
@app.route('/playlists')
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-tokens')
    
    header = {
        'Authorization' : f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me/playlists', headers = header)
    playlist = response.json()
    global user_playlists  # Declare user_playlists as global
    for item in playlist['items']:
        user_playlists[item['name']] = item['id']
    return (redirect('/playlist'))
@app.route('/playlist')
def get_userinput():
    print("Please enter which playlist you would like to convert: ")
    for names in user_playlists:
        print(names)
    return redirect('user_choice')

@app.route('/user_choice')
def display_user_choice():
    user_input = input
    if user_input in user_playlists:
        return print(user_playlists[user_input])
    return('/user_choice')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)