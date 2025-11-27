from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # 之後可以換成更安全的

    @app.route('/')
    def index():
        return "Hello Photography Blog!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)