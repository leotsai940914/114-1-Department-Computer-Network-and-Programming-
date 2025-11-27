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
            # 將 DB 回傳的 tuple list 攤平成字串 list 方便前端使用
            products = db.get_product_names_by_category(category)
            flat_products = [p[0] if isinstance(p, (list, tuple)) else p for p in products]
            return jsonify({"product": flat_products})

        if product_name:
            return jsonify({"price": db.get_product_price(product_name)})

        return jsonify({"error": "Missing parameter"}), 400

    elif request.method == 'POST':
        def form_value(*keys, default=None):
            for k in keys:
                val = request.form.get(k)
                if val not in (None, ""):
                    return val
            return default

        order_data = {
            "product_date": form_value("product_date", "product-date"),
            "customer_name": form_value("customer_name", "customer-name"),
            "product_name": form_value("product_name", "product-name"),
            "product_amount": int(form_value("product_amount", "product-amount", default=0)),
            "product_total": int(form_value("product_total", "product-total", default=0)),
            "product_status": form_value("product_status", "product-status", default="未付款"),
            "product_note": form_value("product_note", "product-note", default=""),
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
