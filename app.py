import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Fetch environment variables safely
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# Build the exact endpoints and headers for Supabase's REST API
TABLE_URL = f"{SUPABASE_URL}/rest/v1/names"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

@app.route('/')
def index():
    return render_template('index.html', names=[])

@app.route('/save', methods=['POST'])
def save_name():
    name_to_save = request.form.get('username')
    if name_to_save:
        try:
            # Data payload to send to the database
            data = {"name": name_to_save}
            # Send a direct POST request to insert the row
            requests.post(TABLE_URL, json=data, headers=HEADERS)
        except Exception as e:
            print(f"Error saving data: {e}")
    return redirect(url_for('index'))

@app.route('/show', methods=['GET'])
def show_names():
    all_names = []
    try:
        # Send a direct GET request to pull all records sorted alphabetically or sequentially
        response = requests.get(f"{TABLE_URL}?select=name", headers=HEADERS)
        if response.status_code == 200:
            all_names = response.json()
        else:
            all_names = [{"name": f"Database error: {response.text}"}]
    except Exception as e:
        print(f"Error fetching data: {e}")
        all_names = [{"name": f"Connection error: {e}"}]
        
    return render_template('index.html', names=all_names)

if __name__ == '__main__':
    app.run(debug=True)
