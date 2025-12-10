from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.user_model import UserModel

# 先宣告 Blueprint（非常重要）
auth_bp = Blueprint("auth_routes", __name__)


# ------------------------------
# 註冊 Register
# ------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()

        # 基本欄位檢查
        if not username or not email or not password:
            return render_template("register.html", error="請填寫所有欄位")

        # 檢查帳號 / Email 是否重複
        if UserModel.find_by_username(username):
            return render_template("register.html", error="帳號已被註冊")
        if UserModel.find_by_email(email):
            return render_template("register.html", error="Email 已被註冊")

        # 建立使用者（密碼哈希）
        password_hash = generate_password_hash(password)
        UserModel.create_user(username, email, password_hash)

        # 註冊成功 → 導向登入頁
        return redirect(url_for("auth_routes.login"))

    # GET：回傳註冊頁
    return render_template("register.html")


# ------------------------------
# 登出 Logout
# ------------------------------
@auth_bp.route("/logout")
def logout():
    session.clear()   # 清空 session
    return redirect(url_for("auth_routes.login"))


# ------------------------------
# 登入 Login
# ------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # 檢查帳號是否存在
        user = UserModel.find_by_username(username)
        if not user:
            return render_template("login.html", error="帳號不存在")

        # 密碼是否正確
        if not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="密碼錯誤")

        # 登入成功 → 寫入 session
        session["user_id"] = user["id"]
        session["role"] = user["role"]

        return redirect(url_for("post_routes.home"))

    # GET 請求：回傳登入頁
    return render_template("login.html")
