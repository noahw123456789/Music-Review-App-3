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
            cursor = conn.cursor()

            conn.execute(''' INSERT INTO ratings (ratings.rating_id, ratings.song_id, ratings.rating, ratings.listen_again, ratings.other_songs_by_artist, ratings.lyrics_rating, ratings.mood, songs.song_title) VALUES (?, ?, ?, ?, ?, ?)
                        JOIN songs ON ratings.song_id = songs.id '''
                        (rating, listen_again, mood, other_songs_by_artist, lyrics_rating, id))

            conn.commit()
            cursor.close()  # Close the cursor immediately after use
            conn.close()  # Close the connection immediately after use
            return redirect(url_for('view_ratings'))

    conn.close()
    return render_template('song_rating.html', song=song)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_rating(id):
    conn = get_db_connection()
    rating = conn.execute('SELECT * FROM ratings WHERE rating_id = ?', (id,)).fetchone()
    if request.method == 'POST':
        rating_value = request.form.get('rating')
        listen_again = request.form.get('listen_again')
        mood = request.form.get('mood')
        other_songs_by_artist = request.form.get('other_songs_by_artist')
        lyrics_rating = request.form.get('lyrics_rating')
        if not rating_value or not listen_again or not mood or not other_songs_by_artist or not lyrics_rating:
            flash('Please fill out all fields!')
        else:
            cursor = conn.cursor()  # Open a new cursor
            cursor.execute('UPDATE ratings SET rating = ?, listen_again = ?, mood = ?, other_songs_by_artist = ?, lyrics_rating = ? WHERE rating_id = ?',
                           (rating_value, listen_again, mood, other_songs_by_artist, lyrics_rating, id))
            conn.commit()
            cursor.close()  # Close the cursor immediately after use
            conn.close()  # Close the connection immediately after use
            return redirect(url_for('view_ratings'))
    conn.close()
    return render_template('edit_rating.html', rating=rating)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_game(id):
    # Connect to the database
    conn = get_db_connection()
    # Execute the DELETE statement
    conn.execute('DELETE FROM games WHERE id = ?', (id,))
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()
    # Redirect to the 'view_games' page
    return redirect(url_for('view_games'))

@app.route('/ratings')
def view_ratings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ratings.rating_id, ratings.song_id, ratings.rating, ratings.listen_again,
               ratings.other_songs_by_artist, ratings.lyrics_rating, ratings.mood, songs.song_title
        FROM ratings
        JOIN songs ON ratings.song_id = songs.id
    """)
    ratings = cursor.fetchall()
    cursor.close()  # Close the cursor immediately after use
    conn.close()  # Close the connection immediately after use
    return render_template('view_ratings.html', ratings=ratings)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
