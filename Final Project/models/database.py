import sqlite3
from flask import current_app


def get_db_connection():
    """讀取 Flask app 的 Config 設定來取得資料庫路徑"""
    db_path = current_app.config["DATABASE_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 以 dict 方式讀資料
    return conn


def create_tables():
    """建立資料表"""
    conn = get_db_connection()
    cur = conn.cursor()

    # users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'visitor'
        );
    """)

    # categories
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """)

    # posts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            cover_image_url TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    # comments
    cur.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            nickname TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id)
        );
    """)
    # settings（全站僅一筆 id=1）
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            site_title TEXT,
            subtitle TEXT,
            footer_text TEXT,
            about_html TEXT,
            avatar_url TEXT,
            featured_post_id INTEGER,
            featured_tagline TEXT
        );
    """)

    # 若舊版 settings 表尚未有新欄位，動態補上
    cur.execute("PRAGMA table_info(settings)")
    cols = {row["name"] for row in cur.fetchall()}
    if "featured_post_id" not in cols:
        cur.execute("ALTER TABLE settings ADD COLUMN featured_post_id INTEGER")
    if "featured_tagline" not in cols:
        cur.execute("ALTER TABLE settings ADD COLUMN featured_tagline TEXT")

    # 若沒有資料 → 建立預設設定
    cur.execute("SELECT COUNT(*) AS cnt FROM settings")
    count = cur.fetchone()["cnt"]

    if count == 0:
        cur.execute("""
            INSERT INTO settings (id, site_title, subtitle, footer_text, about_html, avatar_url, featured_post_id, featured_tagline)
            VALUES (
                1,
                'LumenFilm',
                '電影觀影筆記與影像解析',
                '寫下每一部電影留給我們的影像與思考',
                '<p>這裡是我的電影觀影與影像拆解筆記。</p>',
                'https://i.imgur.com/placeholder.jpg',
                NULL,
                '本週主打文章'
            )
        """)

    conn.commit()
    conn.close()


def init_categories():
    """初始化六個分類"""
    conn = get_db_connection()
    cur = conn.cursor()

    default_categories = [
        "Review",
        "Scene Analysis",
        "Themes",
        "Character Study",
        "Film Theory",
        "Directors"
    ]

    for cat in default_categories:
        cur.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))

    conn.commit()
    conn.close()
