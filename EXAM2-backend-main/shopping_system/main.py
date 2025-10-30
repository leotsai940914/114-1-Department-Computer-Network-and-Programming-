from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from datetime import datetime
import sqlite3
import logging
import re 
import os


app = Flask(__name__)

app.secret_key = 'your_very_secret_key_change_this'

# 路徑修改
def get_db_connection():
    conn = sqlite3.connect('shopping_data.db')
    if not os.path.exists('shopping_data.db'):
        logging.error(f"Database file not found at {'shopping_data.db'}")
        return None
    conn.row_factory = sqlite3.Row
    return conn

# 補齊空缺程式碼
@app.route('/')
def index():
    # 檢查 'username' 是否存在於 'session' (伺服器的記憶) 中
    if 'username' not in session:
        # 如果使用者「尚未登入」，就將他們「重新導向」到 'page_login' (登入頁面)
        return redirect(url_for('page_login'))
    
    # 如果 'username' 存在 (已登入)，才顯示購物介面
    return render_template('index.html')
    
@app.route('/page_register', methods=['GET', 'POST'])
def page_register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email') 

        # 密碼驗證: 8 位以上
        if len(password) < 8:
            return jsonify({"status": "error", "message": "密碼必須超過8個字元"})
        
        # 密碼驗證: 包含英文大小寫
        if not re.search(r'[a-z]', password) or not re.search(r'[A-Z]', password):
            return jsonify({"status": "error", "message": "密碼必須包含英文大小寫"})

        # 信箱驗證: XXX@gmail.com 格式
        if not re.match(r'[^@]+@gmail\.com', email):
            return jsonify({"status": "error", "message": "Email 格式不符重新輸入"})

        # 資料庫操作：檢查帳號重複並寫入
        conn = None
        try:
            conn = get_db_connection()
            if conn is None:
                return jsonify({"status": "error", "message": "資料庫連線失敗"})
            
            cursor = conn.cursor()

            # 檢查帳號是否已存在 (修正 1)
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                # 帳號已存在
                return jsonify({"status": "error", "message": "帳號已存在，成功修改密碼或信箱"})

            # 寫入新資料 (修正 2)
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                           (username, password, email))
            conn.commit()

            # 註冊成功
            return jsonify({"status": "success", "message": "註冊成功"})

        except sqlite3.Error as e:
            return jsonify({"status": "error", "message": f"資料庫錯誤: {e}"})
        
        finally:
            if conn:
                conn.close()
       
    return render_template('page_register.html')


def login_user(username, password):
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                return {"status": "success", "message": "Login successful"}
            else:
                return {"status": "error", "message": "Invalid username or password"}
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return {"status": "error", "message": "An error occurred"}
        finally:
            conn.close()
    else:
        return {"status": "error", "message": "Database connection error"}

@app.route('/page_login' , methods=['GET', 'POST'])
def page_login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            result = login_user(username, password)
            if result["status"] == "success":
                session['username'] = username
            return jsonify(result)
        return render_template('page_login.html')
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 補齊剩餘副程式
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('page_login'))

# 最後的 API (Python 購物介面 30%)
@app.route('/place_order', methods=['POST'])
def place_order():
    # 1. 檢查使用者是否登入
    if 'username' not in session:
        return jsonify({"status": "error", "message": "請先登入"}), 401

    conn = None
    try:
        # 2. 獲取 JS 傳來的訂單列表
        data = request.get_json()
        items = data.get('items') # 記得 JS 是傳 'items'
        
        # 3. 獲取目前時間 (符合作業 alert 範例)
        now = datetime.now()
        # 格式化日期 '2025-10-29'
        order_date_str = now.strftime('%Y-%m-%d')
        # 格式化時間 '21:59'
        order_time_str = now.strftime('%H:%M') 
        
        conn = get_db_connection()
        if conn is None:
            return jsonify({"status": "error", "message": "資料庫連線失敗"})
        
        cursor = conn.cursor()

        total_order_amount = 0
        alert_message_items = [] # 準備用來放 "T-Shirt: ..."

        # 4. (作業要求 4) 將資料寫入資料庫
        for item in items:
            product_name = item.get('name')
            price = item.get('price')
            quantity = item.get('qty')
            total_price = item.get('total')

            # 寫入 'shop_list_table' (使用 .db 檔案中的正確名稱)
            cursor.execute(
                """
                INSERT INTO shop_list_table 
                (Product, Price, Number, "Total Price", Date, Time)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (product_name, price, quantity, total_price, order_date_str, order_time_str)
            )

            #準備 alert 訊息
            total_order_amount += total_price
            alert_message_items.append(
                f" {product_name}:  {price} NT/件 x{quantity}  共 {total_price} NT "
            )

        conn.commit() # 執行所有 SQL 寫入

        # 6. 組合完整的 alert 訊息
        items_details = "\n".join(alert_message_items)
        final_message = f"""{order_time_str}，已成功下單:
{items_details}
此單花費總金額: {total_order_amount} NT"""

        return jsonify({"status": "success", "message": final_message})

    except sqlite3.Error as e:
        # 處理資料庫 UNIQUE constraint failed (如果 Product 是 PRIMARY KEY)
        if "UNIQUE constraint failed" in str(e):
             return jsonify({"status": "error", "message": "訂單中已有重複商品 (主鍵衝突)，請重新下單"})
        return jsonify({"status": "error", "message": f"資料庫錯誤: {e}"})
    
    finally:
        if conn:
            conn.close()

# 補齊空缺程式碼
if __name__ == '__main__':
    app.run(debug=True)