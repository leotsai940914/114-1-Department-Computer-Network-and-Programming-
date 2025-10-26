from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_very_secret_key_12345'

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    # 檢查請求方法
    if request.method == 'POST':
        username_from_form = request.form['username']
        password_from_form = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = "SELECT * FROM teachers WHERE username = ? AND password = ?"
        c.execute(query, (username_from_form, password_from_form))
        teacher = c.fetchone()
        conn.close()

        if teacher:
            session['username'] = username_from_form
            return redirect(url_for('grades'))
        else:
            error = "錯誤的名稱或錯誤的密碼"

        
    return render_template('login.html', error=error)


@app.route('/grades')
def grades():
    if 'username' not in session:
        return redirect(url_for('login'))
    logged_in_user = session['username']
    return render_template('grades.html', username=logged_in_user)


if  __name__ == '__main__':
    app.run(debug=True)


