import datetime
import os
import random
import sqlite3 #新增

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

    def get_product_names_by_category(self, category):
        pass

    def get_product_price(self, product):
        pass

    def add_order(self, order_data):
        pass

    def get_all_orders(self):
        # 之後會改成真的去查 SQLite
        # 現在先回傳空 list，讓模板可以安全地 for 迴圈
        return []

    def delete_order(self, order_id):
        pass