from models.database import get_db_connection
from datetime import datetime


class PostModel:

    @staticmethod
    def create_post(title, content, category_id, user_id, cover_image_url=None, status="published"):
        """Create a new post with timestamp."""
        conn = get_db_connection()
        cursor = conn.cursor()

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO posts (title, content, category_id, user_id, created_at, cover_image_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, content, category_id, user_id, created_at, cover_image_url, status))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id


    @staticmethod
    def get_all_posts(include_unpublished=False):
        """Fetch all posts with category name."""
        conn = get_db_connection()
        cursor = conn.cursor()

        base_sql = """
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
        """
        if include_unpublished:
            base_sql += " ORDER BY created_at DESC"
            cursor.execute(base_sql)
        else:
            base_sql += " WHERE status = 'published' ORDER BY created_at DESC"
            cursor.execute(base_sql)

        posts = cursor.fetchall()
        conn.close()
        return posts


    @staticmethod
    def get_all_posts_paginated(limit, offset):
        """Fetch all published posts with pagination."""
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
            WHERE status = 'published'
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(sql, (limit, offset))
        posts = cursor.fetchall()

        count_sql = "SELECT COUNT(*) as valid_count FROM posts WHERE status = 'published'"
        cursor.execute(count_sql)
        total = cursor.fetchone()["valid_count"]

        conn.close()
        return posts, total


    @staticmethod
    def search_posts(query):
        """Search published posts by title or content."""
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
            WHERE status = 'published'
            AND (title LIKE ? OR content LIKE ?)
            ORDER BY created_at DESC
        """
        like_query = f"%{query}%"
        cursor.execute(sql, (like_query, like_query))
        posts = cursor.fetchall()
        conn.close()
        return posts


    @staticmethod
    def get_posts_by_category(category_id, include_unpublished=False):
        """Fetch posts filtered by category ID."""
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
            WHERE category_id = ?
        """
        params = [category_id]
        if not include_unpublished:
            sql += " AND status = 'published'"
        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)

        posts = cursor.fetchall()
        conn.close()
        return posts

    @staticmethod
    def get_posts_by_user(user_id, include_unpublished=False):
        """Fetch posts by author."""
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
            WHERE user_id = ?
        """
        params = [user_id]
        if not include_unpublished:
            sql += " AND status = 'published'"
        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_posts_by_user_paginated(user_id, limit, offset, include_unpublished=False):
        conn = get_db_connection()
        cur = conn.cursor()
        sql = """
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
            WHERE user_id = ?
        """
        params = [user_id]
        if not include_unpublished:
            sql += " AND status = 'published'"
        sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cur.execute(sql, params)
        rows = cur.fetchall()

        count_sql = "SELECT COUNT(*) AS cnt FROM posts WHERE user_id = ?"
        count_params = [user_id]
        if not include_unpublished:
            count_sql += " AND status = 'published'"
        cur.execute(count_sql, count_params)
        total = cur.fetchone()["cnt"]
        conn.close()
        return rows, total


    @staticmethod
    def get_post_by_id(post_id):
        """Fetch a single post by ID."""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT posts.*, categories.name AS category_name, users.username AS author_name, users.avatar_url AS author_avatar, users.bio AS author_bio
            FROM posts
            JOIN categories ON posts.category_id = categories.id
            JOIN users ON posts.user_id = users.id
            WHERE posts.id = ?
        """, (post_id,))

        post = cursor.fetchone()
        conn.close()
        return post
    
    @staticmethod
    def delete_post(post_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update_post(post_id, title, content, category_id, cover_image_url):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE posts
            SET title = ?, content = ?, category_id = ?, cover_image_url = ?
            WHERE id = ?
        """, (title, content, category_id, cover_image_url, post_id))

        conn.commit()
        conn.close()

    @staticmethod
    def update_status(post_id, status):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE posts SET status = ? WHERE id = ?", (status, post_id))
        conn.commit()
        conn.close()
