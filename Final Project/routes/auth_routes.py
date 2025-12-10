from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.user_model import UserModel

auth_bp = Blueprint("auth_routes", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # --- 基本欄位檢查 ---
        if not username or not email or not password:
            return render_template("register.html", error="所有欄位皆為必填")

        # --- 檢查 username 是否存在 ---
        existing_user = UserModel.find_by_username(username)
        if existing_user:
            return render_template("register.html", error="此帳號已被使用")

        # --- 檢查 email 是否存在 ---
        existing_email = UserModel.find_by_email(email)
        if existing_email:
            return render_template("register.html", error="Email 已被註冊")

        # --- 密碼 hash ---
        password_hash = generate_password_hash(password)

        # --- 寫入資料庫 ---
        UserModel.create_user(username, email, password_hash)

        # 註冊成功 → redirect 到登入頁
        return redirect(url_for("auth_routes.login"))

    # GET：顯示註冊頁
    return render_template("register.html")