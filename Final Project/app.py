from flask import Flask, render_template
from markupsafe import Markup, escape
from routes.auth_routes import auth_bp
from routes.post_routes import post_bp
from routes.category_routes import category_bp
from routes.comment_routes import comment_bp
from models.database import create_tables, init_categories
from models.post_model import PostModel


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-change-later"

    # Blueprint 註冊
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)

    # 建立資料表 & 初始化分類
    create_tables()
    init_categories()

    # Jinja filter：將換行轉換為 <br>
    @app.template_filter("nl2br")
    def nl2br(value):
        return Markup("<br>".join(escape(value).split("\n")))

    # 首頁
    @app.route("/")
    def index():
        posts = PostModel.get_all_posts()
        return render_template("index.html", posts=posts)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
