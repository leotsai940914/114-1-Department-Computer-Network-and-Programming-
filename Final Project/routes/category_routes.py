from flask import Blueprint, render_template
from models.category_model import CategoryModel
from models.post_model import PostModel

category_bp = Blueprint("category_routes", __name__)


# =============================
# 分類一覽頁
# =============================
@category_bp.route("/categories")
def categories_index():
    categories = CategoryModel.get_all_categories()
    return render_template("categories_index.html", categories=categories)


# =============================
# 分類頁：顯示該分類所有文章
# =============================
@category_bp.route("/category/<name>")
def category_page(name):
    category = CategoryModel.get_category_by_name(name)

    if not category:
        return render_template("error.html", message="分類不存在"), 404

    posts = PostModel.get_posts_by_category(category["id"])

    return render_template(
        "category_posts.html",
        category_name=category["name"],   # 使用 DB 版本名稱
        posts=posts
    )


# =============================
# About 頁面
# =============================
@category_bp.route("/about")
def about():
    return render_template("about.html")