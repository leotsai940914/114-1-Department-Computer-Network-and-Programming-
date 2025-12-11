# routes/__init__.py
# 支援套件匯入與直接執行（避免 IDE 直跑檔案時找不到 package）
try:
    from .auth_routes import auth_bp
    from .post_routes import post_bp
    from .category_routes import category_bp
    from .comment_routes import comment_bp
    from .admin_routes import admin_bp
except ImportError:  # pragma: no cover
    from routes.auth_routes import auth_bp
    from routes.post_routes import post_bp
    from routes.category_routes import category_bp
    from routes.comment_routes import comment_bp
    from routes.admin_routes import admin_bp

__all__ = [
    "auth_bp",
    "post_bp",
    "category_bp",
    "comment_bp",
    "admin_bp",
]
