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
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return render_template('index.html', songs=songs)

@app.route('/songs')
def all_songs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()
    conn.close()
    return render_template('all_songs.html', songs=songs)

@app.route('/rate/<int:id>', methods=['GET', 'POST'])
def song_rating(id):
    conn = get_db_connection()
    song = conn.execute('SELECT * FROM songs WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        song_rating = request.form.get('song_rating')
        listen_again = request.form.get('listen_again')
        recommend = request.form.get('recommend')
        other_songs_by_artist = request.form.get('other_songs_by_artist')
        lyrics_rating = request.form.get('lyrics_rating')
        guessed_genre = request.form.get('guessed_genre')

        if not song_rating or not listen_again or not recommend or not other_songs_by_artist or not lyrics_rating or not guessed_genre:
            flash('Please fill out all fields!')
        else:
            conn.execute('INSERT INTO users-ratings (song_id, song_rating, listen_again, recommend, other_songs_by_artist, lyrics_rating, guessed_genre) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (id, song_rating, listen_again, recommend, other_songs_by_artist, lyrics_rating, guessed_genre))
            conn.commit()
            conn.close()
            return redirect(url_for('all_songs'))

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
