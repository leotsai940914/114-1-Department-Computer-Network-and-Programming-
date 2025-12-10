from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user_model import UserModel

# 先宣告 Blueprint（非常重要）
auth_bp = Blueprint("auth_routes", __name__)


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