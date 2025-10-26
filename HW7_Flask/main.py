# 引入工具
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

# 建立 app 和 secret key
app = Flask(__name__)
app.secret_key = 'your_very_secret_key_12345'


#login 路由
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


@app.route('/grades', methods=['GET', 'POST'])
def grades():
    # 安全檢查
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # 從 session 裡把名字拿出來
    logged_in_user = session['username']

    # 檢查請求為 POST 還是 GET
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        score = request.form['score']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = "INSERT INTO grades (name, student_id, score) VALUES (?, ?, ?)"

        c.execute(query, (name, student_id, score))

        conn.commit()
        conn.close()
        return redirect(url_for('grades'))

    else:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = "SELECT name, student_id, score FROM grades ORDER BY student_id ASC"
        c.execute(query)
        all_grades = c.fetchall()
        conn.close()

        return render_template(
            'grades.html', 
            username=logged_in_user,
            grades_list=all_grades
        )

@app.route('/delete', methods=['POST'])
def delete_grade():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method =='POST':
        student_id_to_delete = request.form['delete_id']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        query = "DELETE FROM grades WHERE student_id = ?"
        c.execute(query, (student_id_to_delete,))

        conn.commit()

        conn.close()

    return redirect(url_for('grades'))



if  __name__ == '__main__':
    app.run(debug=True, port=5001)


