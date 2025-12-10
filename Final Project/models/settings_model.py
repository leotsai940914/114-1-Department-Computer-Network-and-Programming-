# models/settings_model.py

from models.database import get_db_connection


class SettingsModel:
    @staticmethod
    def get_settings():
        """讀取單筆設定，若不存在則建立預設值。"""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM settings WHERE id = 1")
        data = cur.fetchone()

        if not data:
            cur.execute("""
                INSERT INTO settings (id, site_title, subtitle, footer_text, about_html, avatar_url)
                VALUES (
                    1,
                    'LumenFilm',
                    '電影觀影筆記與影像解析',
                    '寫下每一部電影留給我們的影像與思考',
                    '<p>這裡是我的電影觀影與影像拆解筆記。</p>',
                    'https://i.imgur.com/placeholder.jpg'
                )
            """)
            conn.commit()
            cur.execute("SELECT * FROM settings WHERE id = 1")
            data = cur.fetchone()

        conn.close()
        return data

    @staticmethod
    def update_settings(site_title, subtitle, footer_text, about_html, avatar_url):
        """更新單筆設定，欄位與 settings 資料表一致。"""
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE settings
            SET site_title = ?,
                subtitle = ?,
                footer_text = ?,
                about_html = ?,
                avatar_url = ?
            WHERE id = 1
        """, (site_title, subtitle, footer_text, about_html, avatar_url))

        conn.commit()
        conn.close()
