import re
import sqlite3

DB_PATH = "users.db"

# 連線資料庫
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            name TEXT NOT NULL,
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 驗證email
def validate_email(email: str) -> bool:
    pattern = r'^[A-Za-z0-9._%+-]+@gmail\.com$'
    return bool(re.match(pattern, email))

# 驗證密碼強度
def validate_password(pw: str) -> bool:
    # 至少 8 字、含大小寫、特殊字元、不能連號
    if len(pw) < 8:
        print("❌ 密碼必須超過 8 個字元")
        return False
    if not re.search(r'[A-Z]', pw):
        print("❌ 密碼需包含大寫英文字母")
        return False
    if not re.search(r'[a-z]', pw):
        print("❌ 密碼需包含小寫英文字母")
        return False
    if not re.search(r'[^A-Za-z0-9]', pw):
        print("❌ 密碼需包含至少一個特殊字元")
        return False
    if re.search(r'(123|234|345|456|567|678|789|abc|bcd|cde)', pw.lower()):
        print("❌ 密碼不可包含連號（如123、abc）")
        return False
    return True


    