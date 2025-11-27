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

    orders = db.get_all_orders()

    conn.close()

    warning = request.args.get("warning")
    return render_template('form.html', orders=orders, warning=warning)


# ---------- PRODUCT ROUTE ----------
@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    if request.method == 'GET':
        category = request.args.get("category")
        product_name = request.args.get("product")

        if category:
            return jsonify({"product": db.get_product_names_by_category(category)})

        if product_name:
            return jsonify({"price": db.get_product_price(product_name)})

        return jsonify({"error": "Missing parameter"}), 400

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

        db.add_order(order_data)
        return redirect(url_for("index", warning="Order placed successfully"))

    elif request.method == 'DELETE':
        order_id = request.args.get("order_id")

        if not order_id:
            return jsonify({"error": "order_id is required"}), 400

        success = db.delete_order(order_id)

        if success:
            return jsonify({"message": "Order deleted successfully"}), 200
        else:
            return jsonify({"message": "Order not found"}), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)