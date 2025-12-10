from models.database import get_db_connection
from datetime import datetime

class CommentModel:

    @staticmethod
    def create_comment(post_id, nickname, content):
        conn = get_db_connection()
        cur = conn.cursor()

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            INSERT INTO comments (post_id, nickname, content, created_at)
            VALUES (?, ?, ?, ?)
        """, (post_id, nickname, content, created_at))

        conn.commit()
        conn.close()

    @staticmethod
    def get_comments_by_post(post_id):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM comments
            WHERE post_id = ?
            ORDER BY created_at DESC
        """, (post_id,))

        comments = cur.fetchall()
        conn.close()
        return comments