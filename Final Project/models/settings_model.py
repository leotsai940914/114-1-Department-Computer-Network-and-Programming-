# models/settings_model.py

from models.database import get_db_connection

class SettingsModel:

    @staticmethod
    def init_settings():
        """確保 settings 表至少有 1 筆資料"""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                site_title TEXT NOT NULL,
                subtitle TEXT,
                avatar_url TEXT,
                about TEXT
            );
        """)

        # 如果沒有資料 → 建立預設值
        cur.execute("SELECT COUNT(*) FROM settings")
        exists = cur.fetchone()[0]

        if exists == 0:
            cur.execute("""
                INSERT INTO settings (id, site_title, subtitle, avatar_url, about)
                VALUES (1, 'LumenFilm', '電影觀影筆記與影像解析', NULL, '歡迎來到 LumenFilm')
            """)

        conn.commit()
        conn.close()

    @staticmethod
    def get_settings():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM settings WHERE id = 1")
        data = cur.fetchone()
        conn.close()
        return data

    @staticmethod
    def update_settings(site_title, subtitle, avatar_url, about):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE settings
            SET site_title=?, subtitle=?, avatar_url=?, about=?
            WHERE id = 1
        """, (site_title, subtitle, avatar_url, about))

        conn.commit()
        conn.close()