from flask import Blueprint, render_template
from models.category_model import CategoryModel
from models.post_model import PostModel

category_bp = Blueprint("category_routes", __name__)


@category_bp.route("/category/<name>")
def category_posts(name):
    category = CategoryModel.get_category_by_name(name)

    if not category:
        return render_template("error.html", message="分類不存在"), 404

    posts = PostModel.get_posts_by_category(category["id"])

    return render_template(
        "category_posts.html",
        category_name=name,
        posts=posts
    )
