from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        orders = db.get_all_orders()
        if request.args.get('warning'):
            warning = request.args.get('warning')
            return render_template('form.html', orders=orders, warning=warning)
        return render_template('form.html', orders=orders)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():
    # 1. GET：商品列表 or 單價查詢
    if request.method == 'GET':
        category = request.args.get('category')
        product_name = request.args.get('product')

        if category:
            rows = db.get_product_names_by_category(category)
            products = [r[0] for r in rows]
            return jsonify({"product": products})

        elif product_name:
            price = db.get_product_price(product_name)
            return jsonify({"price": price})

        return jsonify({"error": "Missing category or product parameter"}), 400

    # 2. POST：新增訂單
    elif request.method == 'POST':
        product_date = request.form.get('product-date')
        customer_name = request.form.get('customer-name')
        product_name = request.form.get('product-name')
        product_amount_raw = request.form.get('product-amount', '0')
        product_total_raw = request.form.get('product-total', '0')
        product_status = request.form.get('product-status')
        product_note = request.form.get('product-note')

        try:
            product_amount = int(product_amount_raw)
        except:
            product_amount = 0

        try:
            product_total = int(product_total_raw)
        except:
            product_total = 0

        order_data = {
            'product_date': product_date,
            'customer_name': customer_name,
            'product_name': product_name,
            'product_amount': product_amount,
            'product_total': product_total,
            'product_status': product_status,
            'product_note': product_note,
        }

        db.add_order(order_data)
        return redirect(url_for('index', warning="Order placed successfully"))

    # 3. DELETE：刪除訂單
    elif request.method == 'DELETE':
        order_id = request.args.get('order_id')
        if not order_id:
            return jsonify({"error": "order_id is required"}), 400

        db.delete_order(order_id)
        return jsonify({"message": "Order deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)
