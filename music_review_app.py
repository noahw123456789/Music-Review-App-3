from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db_connection():
    conn = sqlite3.connect('musicreview.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/songs')
def all_songs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return render_template('all_songs.html', songs=songs)

@app.route('/rate')
def song_rating():
    conn = get_db_connection()
    cursor = conn.cursor()
    song = cursor.execute('SELECT * FROM songs WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('song_rating.html', song=song)

@app.route('/ratings')
def view_ratings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_ratings")
    ratings = cursor.fetchall()
    conn.close()
    return render_template('view_ratings.html', ratings=ratings)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
