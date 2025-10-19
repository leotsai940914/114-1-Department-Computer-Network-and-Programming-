import os
print("目前連線的資料庫路徑：", os.path.abspath("ID_data.db"))
import sqlite3

# --- A.基礎資料設定 ---
CITY_CODE = {
    "A": "臺北市", "B": "臺中市", "C": "基隆市", "D": "臺南市", "E": "高雄市",
    "F": "新北市", "G": "宜蘭縣", "H": "桃園市", "I": "嘉義市", "J": "新竹縣",
    "K": "苗栗縣", "L": "臺中縣", "M": "南投縣", "N": "彰化縣", "O": "新竹市",
    "P": "雲林縣", "Q": "嘉義縣", "R": "臺南縣", "S": "高雄縣", "T": "屏東縣",
    "U": "花蓮縣", "V": "臺東縣", "W": "金門縣", "X": "澎湖縣", "Y": "陽明山",
    "Z": "連江縣"
}

LETTER_MAP = {
    "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17,
    "I": 34, "J": 18, "K": 19, "L": 20, "M": 21, "N": 22, "O": 35, "P": 23,
    "Q": 24, "R": 25, "S": 26, "T": 27, "U": 28, "V": 29, "W": 32, "X": 30,
    "Y": 31, "Z": 33
}

WEIGHTS = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1]

# --- B. 驗證與補碼邏輯 ---
def check_id(id_str: str) -> bool:
    if len(id_str) != 10 or id_str[0] not in LETTER_MAP:
        return False
    try:
        letter_val = LETTER_MAP[id_str[0]]
        nums = [int(n) for n in id_str[1:]]
        convert = [letter_val // 10, letter_val % 10] + nums
        total = sum(a * b for a, b in zip(convert, WEIGHTS))
        return total % 10 == 0
    except ValueError:
        return False

def generate_checksum(id9: str) -> str:
    for i in range(10):
        candidate = id9 + str(i)
        if check_id(candidate):
            return str(i)
    return None

# --- C. 性別與籍別分類 ---
def gender_type(code: str) -> str:
    return "男性" if code == "1" else "女性" if code == "2" else "未知"

def citizen_type(code: str) -> str:
    mapping = {
        "0": "在臺灣出生之本籍國民",
        "1": "人籍國民，原為外國人",
        "2": "人籍國民，原為無戶籍國民",
        "3": "人籍國民，原為港澳居民",
        "4": "人籍國民，原為大陸地區居民",
        "5": "居留國民",
        "6": "外僑居留",
        "7": "居留外國人",
        "8": "居留港澳",
        "9": "居留大陸"
    }
    return mapping.get(code, "未知")

# --- D. 資料庫處理 ---
def process_database(db_path="ID_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT ID FROM ID_table")
    all_rows = cursor.fetchall()

    valid_ids = []
    deleted_count = 0

    for (id_code,) in all_rows:
        if not id_code:
            continue

        # 若只有9碼，補上最後一碼
        if len(id_code) == 9:
            checksum = generate_checksum(id_code)
            if checksum:
                new_id = id_code + checksum
                cursor.execute("UPDATE ID_table SET ID=? WHERE ID=?", (new_id, id_code))
                id_code = new_id

        # 驗證真假
        if check_id(id_code):
            country = CITY_CODE.get(id_code[0], "未知")
            gender = gender_type(id_code[1])
            citizen = citizen_type(id_code[2])
            cursor.execute(
                "UPDATE ID_table SET country=?, gender=?, citizenship=? WHERE ID=?",
                (country, gender, citizen, id_code)
            )
            valid_ids.append(id_code)
        else:
            try:
                cursor.execute("DELETE FROM ID_table WHERE ID=?", (id_code,))
                deleted_count += 1
            except Exception as e:
                print(f"⚠️ 無法刪除 {id_code}：{e}")

    conn.commit()
    conn.close()

    print(f"\n✅ 有效身分證數量：{len(valid_ids)}")
    print(f"🗑️ 已刪除假資料：{deleted_count}")

# --- E. 主程式 ---
if __name__ == "__main__":
    process_database()

    while True:
        user_input = input("\n請輸入身分證號（或輸入 Q 離開）：").upper()
        if user_input == 'Q':
            break
        if check_id(user_input):
            print("✅ 此身分證為真：")
            print(f"縣市：{CITY_CODE.get(user_input[0], '未知')}")
            print(f"性別：{gender_type(user_input[1])}")
            print(f"籍別：{citizen_type(user_input[2])}")
        else:
            print("❌ 假身分證，請重新輸入。")