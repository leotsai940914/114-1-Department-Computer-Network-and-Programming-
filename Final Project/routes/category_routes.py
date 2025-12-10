from flask import Blueprint, render_template

category_bp = Blueprint("category_routes", __name__)

@category_bp.route("/category/<name>")
def category_posts(name):
    # 暫時用假資料，把名稱塞進模板
    return render_template("category_posts.html", category_name=name)