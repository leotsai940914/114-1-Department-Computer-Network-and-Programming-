from flask import Flask, render_template

# 導入各 Blueprint（之後會在 routes/ 裡建立）
from routes.auth_routes import auth_bp
from routes.post_routes import post_bp
from routes.category_routes import category_bp
from routes.comment_routes import comment_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-key-change-later"

    # ===== 註冊 Blueprints =====
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)

    # ===== 首頁 Route =====
    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)