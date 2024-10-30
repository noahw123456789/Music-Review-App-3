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
        rating = request.form.get('rating')
        listen_again = request.form.get('listen_again')
        mood = request.form.get('mood')
        other_songs_by_artist = request.form.get('other_songs_by_artist')
        lyrics_rating = request.form.get('lyrics_rating')

        if not rating or not listen_again or not mood or not other_songs_by_artist or not lyrics_rating:
            flash('Please fill out all fields!')
        else:
            conn.execute('INSERT INTO users_ratings (rating, listen_again, mood, other_songs_by_artist, lyrics_rating) VALUES (?, ?, ?, ?, ?)',
                        (rating, listen_again, mood, other_songs_by_artist, lyrics_rating))
            conn.commit()
            conn.close()
            return redirect(url_for('view_ratings'))

    conn.close()
    return render_template('song_rating.html', song=song)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_rating(id):
    conn = get_db_connection()
    rating = conn.execute('SELECT * FROM ratings WHERE id = ?', (id)).fetchone()
    
    if request.method == 'POST':
        rating = request.form.get('rating')
        listen_again = request.form.get('listen_again')
        mood = request.form.get('mood')
        other_songs_by_artist = request.form.get('other_songs_by_artist')
        lyrics_rating = request.form.get('lyrics_rating')

        if not rating or not listen_again or not mood or not other_songs_by_artist or not lyrics_rating:
            flash('Please fill out all fields!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE ratings set rating = ?, listen_again = ?, mood = ?, other_songs_by_artist = ?, lyrics_rating = ? WHERE id = ?,
                        (rating, listen_again, mood, other_songs_by_artist, lyrics_rating))
            conn.commit()
            conn.close()

            return redirect(url_for('view_ratings'))

    conn.close()
    return render_template('edit_rating.html', rating=rating )

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_rating(id):
    conn = get_db_connection()

    conn.close()
    return render_template('delete_rating.html')

@app.route('/ratings')
def view_ratings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratings")
    ratings = cursor.fetchall()
    conn.close()
    return render_template('view_ratings.html', ratings=ratings)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
