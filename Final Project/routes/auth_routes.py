from flask import Blueprint, render_template

auth_bp = Blueprint("auth_routes", __name__)

@auth_bp.route("/login")
def login():
    return render_template("login.html")

@auth_bp.route("/register")
def register():
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    return "Logout 功能之後實作"