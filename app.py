import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

# Fetch environment variables safely
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# Initialize client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html', names=[])

@app.route('/save', methods=['POST'])
def save_name():
    name_to_save = request.form.get('username')
    if name_to_save:
        try:
            # Explicitly target the table and insert data
            supabase.table('names').insert({"name": name_to_save}).execute()
        except Exception as e:
            print(f"Error saving data: {e}")
    return redirect(url_for('index'))
@app.route('/show', methods=['GET'])
def show_names():
    try:
        # Fetch records safely
        response = supabase.table('names').select('name').execute()
        all_names = response.data if response.data else []
    except Exception as e:
        print(f"Error fetching data: {e}")
        all_names = [{"name": f"Error loading names: {e}"}]
        
    return render_template('index.html', names=all_names)

if __name__ == '__main__':
    app.run(debug=True)
