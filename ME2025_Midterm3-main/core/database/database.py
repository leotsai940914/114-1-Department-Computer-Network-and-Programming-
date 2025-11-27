import datetime
import os
import random
import sqlite3  # 操作 SQLite 資料庫的標準套件

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)
        self._init_tables()  # ★ 自動建立資料表（確保 test.database 能跑）

    # ★ 自動建立資料表
    def _init_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # 建 commodity
            cur.execute("""
                CREATE TABLE IF NOT EXISTS commodity (
                    product TEXT PRIMARY KEY NOT NULL,
                    category TEXT NOT NULL,
                    price NUMERIC NOT NULL
                ) WITHOUT ROWID;
            """)

            # 建 order_list
            cur.execute("""
                CREATE TABLE IF NOT EXISTS order_list (
                    order_id TEXT PRIMARY KEY,
                    product_date TEXT,
                    customer_name TEXT,
                    product_name TEXT,
                    product_amount INTEGER,
                    product_total INTEGER,
                    product_status TEXT,
                    product_note TEXT
                );
            """)

            conn.commit()

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # 1. 根據種類拿商品名稱列表
    def get_product_names_by_category(self, category):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT product FROM commodity WHERE category = ?",
                (category,)
            )
            rows = cur.fetchall()
        return rows

    # 2. 根據商品拿單價
    def get_product_price(self, product):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT price FROM commodity WHERE product = ?",
                (product,)
            )
            row = cur.fetchone()
        return row[0] if row else None

    # 3. 新增一筆訂單
    def add_order(self, order_data):
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

    # 4. 查全部訂單 + 加入商品價格
    def get_all_orders(self):
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
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM order_list WHERE order_id = ?",
                (order_id,)
            )
            conn.commit()
            return cur.rowcount > 0