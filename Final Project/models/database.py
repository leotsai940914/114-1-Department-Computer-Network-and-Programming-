import sqlite3
import os

DB_PATH = "instance/blog.db"

# 取得資料庫連線
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓資料可以用欄位名稱索引
    return conn


# 建立資料表 schema
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # users 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'visitor'
        );
    """)

    # categories 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """)

    # posts 表
    cursor.execute("""
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

    # comments 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            nickname TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id)
        );
    """)

    conn.commit()
    conn.close()


# 初始化六個分類
def init_categories():
    conn = get_db_connection()
    cursor = conn.cursor()

    default_categories = [
        "Review",
        "Scene Analysis",
        "Themes",
        "Character Study",
        "Film Theory",
        "Directors"
    ]

    for cat in default_categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))

    conn.commit()
    conn.close()