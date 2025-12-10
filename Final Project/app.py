from flask import Flask, render_template
from markupsafe import Markup, escape

# 使用 routes/__init__.py 的公開 API
from routes import auth_bp, post_bp, category_bp, comment_bp

# 使用 models/__init__.py 的公開 API
from models import PostModel

# DB 初始化
from models.database import create_tables, init_categories


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-change-later"

    # ----------------------------
    # Blueprint 註冊（順序可自由）
    # ----------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)

    # ----------------------------
    # 建立資料表與初始化分類
    # ----------------------------
    create_tables()
    init_categories()

    # ----------------------------
    # Jinja filter：換行轉 <br>
    # ----------------------------
    @app.template_filter("nl2br")
    def nl2br(value):
        return Markup("<br>".join(escape(value).split("\n")))

    # ----------------------------
    # 首頁（讀取所有文章）
    # ----------------------------
    @app.route("/")
    def index():
        posts = PostModel.get_all_posts()
        return render_template("index.html", posts=posts)

    return app


# ----------------------------
# 主程式入口
# ----------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)