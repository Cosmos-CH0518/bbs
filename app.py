import os
import requests
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ['SUPABASE_URL']
SUPABASE_API_KEY = os.environ['SUPABASE_API_KEY']
SUPABASE_TABLE = os.environ['SUPABASE_TABLE']

app = Flask(__name__)

def fetch_messages():
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?order=created_at.desc"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else []

def post_message(username, message):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "username": username,
        "message": message
    }
    res = requests.post(url, headers=headers, json=data)
    return res.status_code == 201

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        if username and message:
            post_message(username, message)
        return redirect('/')
    messages = fetch_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
