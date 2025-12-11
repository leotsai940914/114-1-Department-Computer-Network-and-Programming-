import os
import secrets
from flask import Flask, render_template, request, session, abort
from markupsafe import Markup, escape
from config import DevelopmentConfig, ProductionConfig

from routes.auth_routes import auth_bp
from routes.post_routes import post_bp
from routes.category_routes import category_bp
from routes.comment_routes import comment_bp
from routes.admin_routes import admin_bp

from models.database import create_tables, init_categories
from models.post_model import PostModel
from models.settings_model import SettingsModel   # ← 要 import


def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV") or os.getenv("APP_ENV") or "development"
    config_cls = ProductionConfig if env.lower() == "production" else DevelopmentConfig
    app.config.from_object(config_cls)

    # ---------- CSRF 保護 ----------
    def generate_csrf_token():
        token = session.get("_csrf_token")
        if not token:
            token = secrets.token_hex(16)
            session["_csrf_token"] = token
        return token

    @app.before_request
    def csrf_protect():
        if request.method == "POST":
            token = session.get("_csrf_token")
            submitted = request.form.get("_csrf_token") or request.headers.get("X-CSRFToken")
            if not token or token != submitted:
                abort(400, description="Invalid CSRF token")

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generate_csrf_token)

    # ---------- 註冊 Blueprint ----------
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(admin_bp)

    # ---------- 初始化資料庫 ----------
    with app.app_context():
        create_tables()      # 建立 tables & 初始化 settings（id=1）
        init_categories()    # 初始化分類（六個）

    # ---------- 自訂 Jinja Filter ----------
    @app.template_filter("nl2br")
    def nl2br(value):
        return Markup("<br>".join(escape(value).split("\n")))

    # ---------- 首頁 ----------
    @app.route("/")
    def index():
        posts = PostModel.get_all_posts()
        settings = SettingsModel.get_settings()
        hero_post = None
        if settings:
            featured_id = settings["featured_post_id"]
            if featured_id:
                hero_post = PostModel.get_post_by_id(featured_id)
        return render_template("index.html", posts=posts, hero_post=hero_post)

    # ---------- 全站注入 settings ----------
    @app.context_processor
    def inject_settings():
        return dict(settings=SettingsModel.get_settings())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
