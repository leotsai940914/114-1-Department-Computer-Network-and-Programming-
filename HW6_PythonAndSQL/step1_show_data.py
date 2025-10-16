import sqlite3

# 1. 連接資料庫
conn = sqlite3.connect("ID_data.db")
cursor = conn.cursor()

# 2. 顯示資料表有哪些
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("📦 資料表有：", tables)

# 3. 抓第一張表（通常就是 ID_table）
table_name = tables[0][0]

# 4. 顯示前10筆資料
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
rows = cursor.fetchall()
print(f"\n📄 {table_name} 前10筆資料：")
for row in rows:
    print(row)

# 5. 關閉資料庫
conn.close()