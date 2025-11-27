from flask import Flask, render_template, request, jsonify, redirect, url_for
from core.database.database import Database

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET'])
def index():
    orders = db.get_all_orders()
    warning = request.args.get('warning')
    return render_template('form.html', orders=orders, warning=warning)

@app.route('/product', methods=['GET', 'POST', 'DELETE'])
def product():

    # --- GET: 查詢商品或價格 -----------------------------------
    if request.method == 'GET':
        category = request.args.get("category")
        product_name = request.args.get("product")

        if category:
            rows = db.get_product_names_by_category(category)
            product_list = [r[0] for r in rows]
            return jsonify({"product": product_list})

        if product_name:
            price = db.get_product_price(product_name)
            return jsonify({"price": price})

        return jsonify({"error": "Missing parameter"}), 400

    # --- POST: 新增訂單 -----------------------------------
    if request.method == 'POST':
        order_data = {
            'product_date': request.form.get('product_date'),
            'customer_name': request.form.get('customer_name'),
            'product_name': request.form.get('product_name'),
            'product_amount': int(request.form.get('product_amount', 1)),
            'product_total': int(request.form.get('product_total', 0)),
            'product_status': request.form.get('product_status'),
            'product_note': request.form.get('product_note'),
        }
        db.add_order(order_data)
        return redirect(url_for('index', warning="Order placed successfully"))

    # --- DELETE: 刪除訂單 -----------------------------------
    if request.method == 'DELETE':
        order_id = request.args.get("order_id")
        success = db.delete_order(order_id)
        if success:
            return jsonify({"message": "Order deleted successfully"}), 200
        return jsonify({"error": "Order not found"}), 404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5500, debug=True)