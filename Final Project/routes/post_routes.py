from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from models.post_model import PostModel
from models.category_model import CategoryModel
from models.comment_model import CommentModel

post_bp = Blueprint("post_routes", __name__)


# =============================
# 單篇文章頁（含留言）
# =============================
@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = PostModel.get_post_by_id(post_id)
    if not post:
        return render_template("error.html", message="文章不存在"), 404

    comments = CommentModel.get_comments_by_post(post_id)

    return render_template(
        "post_detail.html",
        post=post,
        comments=comments
    )


# =============================
# 新增文章（Admin Only）
# =============================
@post_bp.route("/new_post", methods=["GET", "POST"])
def new_post():
    if session.get("role") != "admin":
        abort(403)

    if request.method == "GET":
        categories = CategoryModel.get_all_categories()
        return render_template("new_post.html", categories=categories)

    # POST
    title = request.form.get("title")
    content = request.form.get("content")
    category_id = request.form.get("category_id")
    cover_image_url = request.form.get("cover_image") or None

    if not title or not content or not category_id:
        categories = CategoryModel.get_all_categories()
        return render_template(
            "new_post.html",
            error="標題、內容與分類皆不得為空",
            categories=categories
        )

    # 分類檢查
    try:
        category_id_int = int(category_id)
    except (TypeError, ValueError):
        category_id_int = None

    if not category_id_int or not CategoryModel.get_category_by_id(category_id_int):
        categories = CategoryModel.get_all_categories()
        return render_template(
            "new_post.html",
            error="分類不存在，請重新選擇",
            categories=categories
        )

    new_id = PostModel.create_post(
        title=title,
        content=content,
        category_id=category_id_int,
        user_id=session["user_id"],
        cover_image_url=cover_image_url
    )

    return redirect(url_for("post_routes.post_detail", post_id=new_id))


# =============================
# 刪除文章（Admin Only）
# =============================
@post_bp.route("/post/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    if session.get("role") != "admin":
        abort(403)

    post = PostModel.get_post_by_id(post_id)
    if not post:
        return render_template("error.html", message="文章不存在"), 404

    PostModel.delete_post(post_id)
    return redirect(url_for("index"))


# =============================
# 編輯文章（Admin Only）— 顯示編輯表單
# =============================
@post_bp.route("/post/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    if session.get("role") != "admin":
        abort(403)

    post = PostModel.get_post_by_id(post_id)
    if not post:
        return render_template("error.html", message="文章不存在"), 404

    categories = CategoryModel.get_all_categories()

    return render_template(
        "edit_post.html",
        post=post,
        categories=categories
    )


# =============================
# 編輯文章（Admin Only）— 接收更新
# =============================
@post_bp.route("/post/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    if session.get("role") != "admin":
        abort(403)

    title = request.form.get("title")
    content = request.form.get("content")
    category_id = request.form.get("category_id")
    cover_image_url = request.form.get("cover_image") or None

    if not title or not content:
        post = PostModel.get_post_by_id(post_id)
        categories = CategoryModel.get_all_categories()
        return render_template(
            "edit_post.html",
            post=post,
            categories=categories,
            error="標題與內容不得為空"
        )

    # 分類檢查
    try:
        category_id_int = int(category_id)
    except (TypeError, ValueError):
        category_id_int = None

    if not category_id_int or not CategoryModel.get_category_by_id(category_id_int):
        post = PostModel.get_post_by_id(post_id)
        categories = CategoryModel.get_all_categories()
        return render_template(
            "edit_post.html",
            post=post,
            categories=categories,
            error="分類不存在，請重新選擇"
        )

    # 更新 DB
    PostModel.update_post(
        post_id=post_id,
        title=title,
        content=content,
        category_id=category_id_int,
        cover_image_url=cover_image_url
    )

    return redirect(url_for("post_routes.post_detail", post_id=post_id))
