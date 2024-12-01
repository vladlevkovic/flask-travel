from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import sqlite3
import binascii
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'gif'}

db_name = 'tours.sqlite3'

def create_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        photo TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price INETEGR NOT NULL
        )
    """)
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS saved_tours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tour_id INTEGER,
                name TEXT,
                description TEXT,
                price INTEGER,
                FOREIGN KEY (tour_id) REFERENCES posts (ID)
            )  
        """
    )
    conn.commit()
    conn.close()

# create_db()

@app.route('/')
def index():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add-tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return redirect(request.url)
        photo = request.files['photo']
        file = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (photo, name, description, price) VALUES (?, ?, ?, ?)', (file, name, description, price))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)

