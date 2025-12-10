from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user_model import UserModel

auth_bp = Blueprint("auth_routes", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # --- 檢查帳號是否存在 ---
        user = UserModel.find_by_username(username)
        if not user:
            return render_template("login.html", error="帳號不存在")

        # --- 檢查密碼是否正確 ---
        if not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="密碼錯誤")

        # --- 登入成功 → 寫入 session ---
        session["user_id"] = user["id"]
        session["role"] = user["role"]

        # 可改成導向首頁（目前使用首頁）
        return redirect(url_for("post_routes.home"))

    # GET：回傳登入頁面
    return render_template("login.html")