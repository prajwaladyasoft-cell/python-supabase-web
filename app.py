import os
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client

app = Flask(__name__)

# Connect to Supabase using Environment Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    return render_template('index.html', names=[])

@app.route('/save', methods=['POST'])
def save_name():
    name_to_save = request.form.get('username')
    if name_to_save:
        # Insert name into Supabase table
        supabase.table('names').insert({"name": name_to_save}).execute()
    return redirect(url_for('index'))

@app.route('/show', methods=['GET'])
def show_names():
    # Fetch all records from Supabase
    response = supabase.table('names').select('*').execute()
    all_names = response.data
    return render_template('index.html', names=all_names)

if __name__ == '__main__':
    app.run(debug=True)
