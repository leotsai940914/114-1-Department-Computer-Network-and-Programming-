import unittest
import os

class TestDeployScript(unittest.TestCase):
    def test_script_existence(self):
        self.assertTrue(os.path.exists("deploy.sh"), "找不到 deploy.sh 檔案")

    def test_script_content(self):
        if not os.path.exists("deploy.sh"):
            return

        with open("deploy.sh", "r", encoding="utf-8") as f:
            content = f.read()

        # 檢查關鍵字作為評分標準
        keywords = [
            ("git clone", "未包含 git clone 指令"),
            (".venv", "未建立或使用名為 .venv 的虛擬環境"),
            ("requirements.txt", "未安裝 requirements.txt"),
            ("git pull", "未包含 git pull 更新指令"),
            ("python3 app.py", "未啟動應用程式 (或 python app.py)"),
            ("if", "未包含條件判斷 (if/else)")
        ]

        for keyword, error_msg in keywords:
            self.assertIn(keyword, content, error_msg)

    def test_shebang(self):
        if not os.path.exists("deploy.sh"):
            return
        with open("deploy.sh", "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        self.assertTrue(first_line.startswith("#!/bin/bash") or first_line.startswith("#!/bin/sh"), "缺少 Shebang宣告")

if __name__ == '__main__':
    unittest.main()