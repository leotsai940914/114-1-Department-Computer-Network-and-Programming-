import sqlite3

#連接資料庫
conn = sqlite3.connect("ID_data.db")
cursor = conn.cursor()

#顯示所有資料表名稱
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("資料表裡面有：", tables)

#抓第一張表的名字
table_name = tables[0][0]

#顯示前十筆資料
cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
rows = cursor.fetchall()

print(f"\n {table_name}表格前10筆資料: ")
for row in rows:
    print(row)

conn.close()
