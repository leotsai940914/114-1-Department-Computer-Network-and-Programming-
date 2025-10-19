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
        print("密碼必須超過 8 個字元")
        return False
    if not re.search(r'[A-Z]', pw):
        print("密碼需包含大寫英文字母")
        return False
    if not re.search(r'[a-z]', pw):
        print("密碼需包含小寫英文字母")
        return False
    if not re.search(r'[^A-Za-z0-9]', pw):
        print("密碼需包含至少一個特殊字元")
        return False
    if re.search(r'(123|234|345|456|567|678|789|abc|bcd|cde)', pw.lower()):
        print("密碼不可包含連號（如123、abc）")
        return False
    return True

def sign_up():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    name = input("請輸入姓名：").strip()
    while not name:
        name = input("姓名不可為空，請重新輸入：").strip()

    # 驗證 Email
    while True:
        email = input("請輸入 Email（需為@gmail.com）：").strip()
        if validate_email(email):
            break
        print("⚠️ Email 格式不符，請重新輸入。")

    # 驗證密碼
    while True:
        password = input("請輸入密碼：").strip()
        if validate_password(password):
            break
        print("請重新輸入符合規範的密碼。")

    # 顯示確認資訊
    print(f"\nsave {name} | {email} | {password} | Y / N ?")
    confirm = input("是否儲存？(Y/N)：").upper()
    if confirm != "Y":
        print("已取消註冊。返回主選單。\n")
        conn.close()
        return

    # 檢查 Email 是否重複
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    exists = cursor.fetchone()

    if exists:
        update = input("此 Email 已存在，是否更新此 Email 資訊？(Y/N)：").upper()
        if update == "Y":
            cursor.execute("UPDATE users SET name=?, password=? WHERE email=?", (name, password, email))
            print("使用者資料已更新成功！")
        else:
            print("已取消更新。返回主選單。")
    else:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        print("新使用者已註冊成功！")

    conn.commit()
    conn.close()

# 登入功能
def sign_in():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    name = input("請輸入姓名：").strip()
    email = input("請輸入 Email：").strip()

    cursor.execute("SELECT * FROM users WHERE name=? AND email=?", (name, email))
    user = cursor.fetchone()

    if not user:
        print("名字或 Email 錯誤。")
        conn.close()
        return

    # 驗證密碼
    while True:
        password = input("請輸入密碼：").strip()
        cursor.execute("SELECT password FROM users WHERE email=?", (email,))
        stored_pw = cursor.fetchone()[0]

        if password == stored_pw:
            print("登入成功！\n")
            break
        else:
            print("密碼錯誤。忘記密碼？(Y/N)")
            choice = input().upper()
            if choice == "Y":
                print("進入註冊模式以重設密碼。\n")
                conn.close()
                sign_up()
                return
            elif choice == "N":
                continue

    conn.close()

# 主選單
def main_menu():
    init_db()
    while True:
        print("\n=== 使用者系統 ===")
        print("(a) Sign Up")
        print("(b) Sign In")
        print("(q) 離開")
        mode = input("請選擇模式：").lower()

        if mode == "a":
            sign_up()
        elif mode == "b":
            sign_in()
        elif mode == "q":
            print("程式結束，再見！")
            break
        else:
            print("無效輸入，請重新選擇。")

if __name__ == "__main__":
    main_menu()
    