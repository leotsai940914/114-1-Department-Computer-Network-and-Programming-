from models.database import get_db_connection

class CategoryModel:
    @staticmethod
    def get_category_by_name(name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE name = ?", (name,))
        return cursor.fetchone()

    @staticmethod
    def get_all_categories():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()

        conn.close()
        return categories