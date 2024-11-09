from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Inicjalizacja bazy danych
DATABASE = 'database/db.sqlite3'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Tworzenie tabeli artykułów (tylko jednorazowo przy pierwszym uruchomieniu)
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles ORDER BY date DESC').fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = '2024-11-09'  # Można użyć np. datetime.now().strftime('%Y-%m-%d')

        conn = get_db_connection()
        conn.execute('INSERT INTO articles (title, content, date) VALUES (?, ?, ?)',
                     (title, content, date))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Proste sprawdzenie logowania
        if username == 'admin' and password == 'password':
            return redirect(url_for('admin'))
        else:
            return "Błędne dane logowania, spróbuj ponownie."
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
