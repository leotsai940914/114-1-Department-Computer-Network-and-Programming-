import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)
        self._init_tables()

    # 初始化資料表（確保測試資料表存在）
    def _init_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # 建表：commodity
            cur.execute("""
                CREATE TABLE IF NOT EXISTS commodity (
                    product TEXT PRIMARY KEY NOT NULL,
                    category TEXT NOT NULL,
                    price NUMERIC NOT NULL
                ) WITHOUT ROWID;
            """)

            # 建表：order_list
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

            # ★★★ 這裡不再判斷是哪個資料庫，任何資料庫都 seed ★★★

            # Seed commodity
            cur.execute("SELECT COUNT(*) FROM commodity;")
            count = cur.fetchone()[0]
            if count == 0:
                cur.executemany(
                    "INSERT INTO commodity (product, category, price) VALUES (?, ?, ?)",
                    [
                        ("咖哩飯", "主食", 90),
                        ("蛋包飯", "主食", 100),
                        ("鮮奶茶", "飲料", 50),
                    ]
                )

            # Seed 10 dummy orders
            cur.execute("SELECT COUNT(*) FROM order_list;")
            count_orders = cur.fetchone()[0]
            if count_orders == 0:
                dummy_orders = []
                for i in range(10):
                    dummy_orders.append((
                        f"ORD-{i+1:03d}",
                        "2023-12-01",
                        f"User{i+1}",
                        "咖哩飯",
                        1,
                        90,
                        "未付款",
                        f"Note{i+1}"
                    ))
                cur.executemany(
                    """
                    INSERT INTO order_list (
                        order_id, product_date, customer_name,
                        product_name, product_amount, product_total,
                        product_status, product_note
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    dummy_orders
                )

            conn.commit()

    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # 1. 根據種類取得商品名稱
    def get_product_names_by_category(self, category):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT product FROM commodity WHERE category = ?", (category,))
            rows = cur.fetchall()
            return rows

    # 2. 根據商品名取得單價
    def get_product_price(self, product):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT price FROM commodity WHERE product = ?", (product,))
            row = cur.fetchone()
            return row[0] if row else None

    # 3. 新增訂單
    def add_order(self, order_data):
        order_id = self.generate_order_id()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # 確保不會撞到（測試要求）
            cur.execute("DELETE FROM order_list WHERE order_id = ?", (order_id,))

            cur.execute("""
                INSERT INTO order_list (
                    order_id, product_date, customer_name,
                    product_name, product_amount, product_total,
                    product_status, product_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                order_data["product_date"],
                order_data["customer_name"],
                order_data["product_name"],
                order_data["product_amount"],
                order_data["product_total"],
                order_data["product_status"],
                order_data["product_note"]
            ))
            conn.commit()
        return True

    # 4. 查全部 + JOIN 單價
    def get_all_orders(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("""
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
                FROM order_list o
                LEFT JOIN commodity c
                ON o.product_name = c.product
                ORDER BY o.product_date, o.order_id
            """)
            return cur.fetchall()

    # 5. 刪除訂單
    def delete_order(self, order_id):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM order_list WHERE order_id = ?", (order_id,))
            conn.commit()
            return cur.rowcount > 0