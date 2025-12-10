from models.database import get_db_connection
from datetime import datetime

class PostModel:

    @staticmethod
    def create_post(title, content, category_id, author_id, cover_image_url=None):
        """Create a new post with timestamp."""
        conn = get_db_connection()
        cursor = conn.cursor()

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO posts (title, content, category_id, author_id, created_at, cover_image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, category_id, author_id, created_at, cover_image_url))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all_posts():
        """Fetch all posts with category name."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT posts.*, categories.name AS category_name
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            ORDER BY created_at DESC
        """)
        posts = cursor.fetchall()

        conn.close()
        return posts

    @staticmethod
    def get_posts_by_category(category_id):
        """Fetch posts filtered by category ID."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT posts.*, categories.name AS category_name
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            WHERE category_id = ?
            ORDER BY created_at DESC
        """, (category_id,))

        posts = cursor.fetchall()

        conn.close()
        return posts

    @staticmethod
    def get_post_by_id(post_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT posts.*, categories.name AS category_name
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            WHERE posts.id = ?
        """, (post_id,))

        post = cursor.fetchone()
        conn.close()
        return post