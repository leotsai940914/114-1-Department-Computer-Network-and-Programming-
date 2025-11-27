#!/bin/bash

REPO_URL="https://github.com/leotsai940914/114-1-Department-Computer-Network-and-Programming-.git"
DIR="ME2025_Midterm3-main"

# 若專案不存在 → 第一次執行：clone + venv + pip install + run
if [ ! -d "$DIR" ]; then
    git clone "$REPO_URL" "$DIR"
    cd "$DIR"

    python3 -m venv .venv
    source .venv/bin/activate

    pip install -r requirements.txt

    python3 app.py &
    exit 0
fi

# 第二次之後：pull 更新版本
cd "$DIR"
git pull

source .venv/bin/activate

# 安裝尚未安裝的套件
pip install -r requirements.txt

# 重啟 app.py
pkill -f app.py
python3 app.py &
