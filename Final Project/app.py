from flask import Flask, render_template
from markupsafe import Markup, escape
from config import DevelopmentConfig

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
    app.config.from_object(DevelopmentConfig)

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
        return render_template("index.html", posts=posts)

    # ---------- 全站注入 settings ----------
    @app.context_processor
    def inject_settings():
        return dict(settings=SettingsModel.get_settings())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
