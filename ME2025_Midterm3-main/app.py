from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database
import sqlite3
import os

app = Flask(__name__)

# 指定資料庫檔案
DB_PATH = os.path.join("core", "database", "order_management.db")
db = Database("order_management.db")

# ---------- INDEX ----------
@app.route('/', methods=['GET'])
def index():
    # 建立資料庫連線
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    orders = db.get_all_orders(cur)

    conn.close()

    warning = request.args.get("warning")
    return render_template('form.html', orders=orders, warning=warning)


# ---------- PRODUCT ROUTE ----------
@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():

    # 建立資料庫連線
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ----- GET -----
    if request.method == 'GET':
        category = request.args.get("category")
        product_name = request.args.get("product")

        # 查商品列表
        if category:
            products = db.get_product_names_by_category(cur, category)
            conn.close()
            return jsonify({"product": products})

        # 查單價
        if product_name:
            price = db.get_product_price(cur, product_name)
            conn.close()
            return jsonify({"price": price})

        conn.close()
        return jsonify({"error": "Missing parameter"}), 400

    # ----- POST -----
    elif request.method == 'POST':
        order_data = {
            "product_date": request.form.get("product_date"),
            "customer_name": request.form.get("customer_name"),
            "product_name": request.form.get("product_name"),
            "product_amount": int(request.form.get("product_amount")),
            "product_total": int(request.form.get("product_total")),
            "product_status": request.form.get("product_status"),
            "product_note": request.form.get("product_note"),
        }

        db.add_order(cur, order_data)
        conn.commit()
        conn.close()

        return redirect(url_for("index", warning="Order placed successfully"))

    # ----- DELETE -----
    elif request.method == 'DELETE':
        order_id = request.args.get("order_id")

        if not order_id:
            conn.close()
            return jsonify({"error": "order_id is required"}), 400

        success = db.delete_order(cur, order_id)
        conn.commit()
        conn.close()

        if success:
            return jsonify({"message": "Order deleted successfully"}), 200
        else:
            return jsonify({"message": "Order not found"}), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)