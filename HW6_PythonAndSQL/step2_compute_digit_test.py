letter_map = {
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16,
    'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
    'O': 35, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28,
    'V': 29, 'W': 32, 'X': 30, 'Y': 31, 'Z': 33
}

weights = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1]

def compute_check_digit(id9):
    if len(id9) != 9:
        return None
    letter = id9[0].upper()
    digits = id9[1:]

    if letter not in letter_map or not digits.isdigit():
        return None
    
    code = str(letter_map[letter])
    first_num = int(code[0])
    second_num = int(code[1])

    all_digits = [first_num,second_num] + [int(d) for d in digits]
    total = sum(a * b for a, b in zip(all_digits, weights))
    check_digit = (10 - total % 10) % 10
    return str(check_digit)

#測試看看
test_ids = ["A12345678", "B23456789", "F98765432", "Z11223344", "W18329849"]

for tid in test_ids:
    cd = compute_check_digit(tid)
    if cd:
        print(f"{tid} ➜ 驗證碼為：{cd}，完整ID：{tid}{cd}")
    else:
        print(f"{tid} ➜ ❌ 格式錯誤")