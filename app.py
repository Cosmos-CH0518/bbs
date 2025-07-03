import requests
from flask import Flask, render_template, request, redirect, flash

# ここにSupabaseの情報を直接書く
SUPABASE_URL = "https://uwbsrcjzlgjmvxhbfpye.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV3YnNyY2p6bGdqbXZ4aGJmcHllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1MzI3ODcsImV4cCI6MjA2NzEwODc4N30.fW1qE12tTropZASR0atxVLOkVV3M9wRV0-JASZ4B6oo"
SUPABASE_TABLE = "posts"

app = Flask(__name__)
app.secret_key = "your-secret-key"

def fetch_messages():
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?order=created_at.desc"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Authorization": f"Bearer {SUPABASE_API_KEY}"
    }
    try:
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code != 200:
            print(f"Supabase取得失敗: {res.status_code} {res.text}")
            return []
        return res.json()
    except Exception as e:
        print(f"Supabase取得例外: {e}")
        return []

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
    try:
        res = requests.post(url, headers=headers, json=data, timeout=5)
        if res.status_code not in (201, 200):
            print(f"Supabase投稿失敗: {res.status_code} {res.text}")
            return False
        return True
    except Exception as e:
        print(f"Supabase投稿例外: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        message = request.form.get('message', '').strip()
        if not username or not message:
            flash('名前とメッセージは必須です', 'error')
        else:
            ok = post_message(username, message)
            if not ok:
                flash('投稿に失敗しました。', 'error')
            else:
                flash('投稿しました', 'success')
        return redirect('/')
    messages = fetch_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
