# routes/__init__.py

from .auth_routes import auth_bp
from .post_routes import post_bp
from .category_routes import category_bp
from .comment_routes import comment_bp

__all__ = [
    "auth_bp",
    "post_bp",
    "category_bp",
    "comment_bp"
]