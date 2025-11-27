import datetime
import os
import random
import sqlite3  # 操作 SQLite 資料庫的標準套件

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # 1. 根據種類拿商品名稱列表
    def get_product_names_by_category(self, category):
        """
        回傳格式：[(product1,), (product2,), ...]
        測試裡會寫 [r[0] for r in results] 來拿名稱字串
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT product FROM commodity WHERE category = ?",
                (category,)
            )
            rows = cur.fetchall()
        return rows

    # 2. 根據商品名稱拿單價
    def get_product_price(self, product):
        """
        回傳單一價格 (int/float)，如果商品不存在則回傳 None
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT price FROM commodity WHERE product = ?",
                (product,)
            )
            row = cur.fetchone()
        if row:
            return row[0]
        return None

    # 3. 新增一筆訂單
    def add_order(self, order_data):
        """
        order_data 格式：
        {
            'product_date': '2023-12-01',
            'customer_name': 'TestUser',
            'product_name': '咖哩飯',
            'product_amount': 2,
            'product_total': 180,
            'product_status': '未付款',
            'product_note': 'Test Note'
        }
        """
        # 讓物件自己產生訂單編號
        order_id = self.generate_order_id()

        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO order_list (
                    order_id,
                    product_date,
                    customer_name,
                    product_name,
                    product_amount,
                    product_total,
                    product_status,
                    product_note
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    order_data['product_date'],
                    order_data['customer_name'],
                    order_data['product_name'],
                    order_data['product_amount'],
                    order_data['product_total'],
                    order_data['product_status'],
                    order_data['product_note'],
                )
            )
            conn.commit()
        return True

    # 4. 取得所有訂單＋把單價一起查回來
    def get_all_orders(self):
        """
        回傳 list，每一筆是 tuple，欄位順序：
        0: order_id
        1: product_date
        2: customer_name
        3: product_name
        4: price          (從 commodity 查來)
        5: product_amount
        6: product_total
        7: product_status
        8: product_note
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    o.order_id,
                    o.product_date,
                    o.customer_name,
                    o.product_name,
                    c.price,
                    o.product_amount,
                    o.product_total,
                    o.product_status,
                    o.product_note
                FROM order_list AS o
                LEFT JOIN commodity AS c
                    ON o.product_name = c.product
                ORDER BY o.rowid
                """
            )
            rows = cur.fetchall()
        return rows

    # 5. 刪除一筆訂單
    def delete_order(self, order_id):
        """
        回傳 True / False 代表有沒有真的刪到資料
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM order_list WHERE order_id = ?",
                (order_id,)
            )
            conn.commit()
            deleted = cur.rowcount > 0
        return deleted