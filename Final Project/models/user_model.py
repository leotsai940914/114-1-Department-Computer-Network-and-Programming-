from models.database import get_db_connection

class UserModel:

    @staticmethod
    def create_user(username, email, password_hash, role="visitor", avatar_url=None, bio=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, avatar_url, bio)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, email, password_hash, role, avatar_url, bio))

        conn.commit()
        conn.close()

    @staticmethod
    def find_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def find_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        conn.close()
        return user

    @staticmethod
    def get_all_authors():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, username, avatar_url, bio FROM users ORDER BY username")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def update_profile(user_id, avatar_url=None, bio=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET avatar_url = ?, bio = ?
            WHERE id = ?
        """, (avatar_url, bio, user_id))
        conn.commit()
        conn.close()
