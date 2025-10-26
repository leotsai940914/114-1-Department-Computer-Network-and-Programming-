from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_very_secret_key_12345'

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username_from_form = request.form['username']
        password_from_form = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        query = "SELECT * FROM teachers WHERE username = ? AND password = ?"

        c.execute(query, (username_from_form, password_from_form))
        teacher = c.fetchone

        conn.close()

def show_login_page():
    return render_template('login.html')

if  __name__ == '__main__':
    app.run(debug=True)