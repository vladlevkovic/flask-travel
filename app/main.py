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

# створення таблиць
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

# перевірка дозволених форматів файлів
def allowed_files(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Головна сторінка з переліком усіх турів
@app.route('/')
def index():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    data = cursor.fetchall()
    print(data)
    conn.close()
    return render_template('index.html', data=data)

# Сторінка для додавання нового туру
@app.route('/add-tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return redirect(request.url)
        photo = request.files['photo']
        if photo and allowed_files(photo.filename):
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

def get_tour_id(tour_id):
    try:
        conn = sqlite3.connect(db_name)
        tour = conn.execute('SELECT * FROM posts WHERE ID = ?', (tour_id))
        print(tour)
        # tour = cursor.execute('SELECT * FROM posts WHERE id = ?', (tour_id))
        conn.close()
        return tour
    except:
        pass

@app.route('/tour/<int:tour_id>/')
def get_tour(tour_id):
    tour = get_tour_id(tour_id)
    print(tour)
    # return render_template('tour.html', tour=tour)

if __name__ == '__main__':
    app.run(debug=True)

