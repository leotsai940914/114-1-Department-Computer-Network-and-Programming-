from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from models.post_model import PostModel
from models.category_model import CategoryModel

post_bp = Blueprint("post_routes", __name__)


# =============================
# 首頁：列出所有文章
# =============================
@post_bp.route("/")
def home():
    posts = PostModel.get_all_posts()
    return render_template("index.html", posts=posts)


# =============================
# 單篇文章頁
# =============================
@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = PostModel.get_post_by_id(post_id)

    if not post:
        return render_template("error.html", message="文章不存在"), 404

    return render_template("post_detail.html", post=post)


# =============================
# 新增文章（僅限 Admin）
# =============================
@post_bp.route("/new_post", methods=["GET", "POST"])
def new_post():
    # --- 權限檢查 ---
    if session.get("role") != "admin":
        abort(403)  # 只有管理者能進來

    # --- GET：顯示表單（需要分類） ---
    if request.method == "GET":
        categories = CategoryModel.get_all_categories()
        return render_template("new_post.html", categories=categories)

    # --- POST：接收表單 ---
    title = request.form.get("title")
    content = request.form.get("content")
    category_id = request.form.get("category_id")
    cover_image_url = request.form.get("cover_image") or None

    # 必填驗證
    if not title or not content:
        categories = CategoryModel.get_all_categories()
        return render_template(
            "new_post.html",
            error="標題與內容不得為空",
            categories=categories
        )

    # --- 寫進資料庫 ---
    new_id = PostModel.create_post(
        title=title,
        content=content,
        category_id=category_id,
        author_id=session["user_id"],
        cover_image_url=cover_image_url
    )

    # --- 導向文章頁 ---
    return redirect(url_for("post_routes.post_detail", post_id=new_id))


# =============================
# 分類頁：顯示某分類的所有文章
# =============================
@post_bp.route("/category/<name>")
def category_page(name):
    category = CategoryModel.get_category_by_name(name)

    if not category:
        return render_template("error.html", message="分類不存在"), 404

    posts = PostModel.get_posts_by_category(category["id"])

    return render_template(
        "category_posts.html",
        category_name=name,
        posts=posts
    )



@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    # 取得文章資料
    post = PostModel.get_post_by_id(post_id)

    if not post:
        return render_template("error.html", message="文章不存在"), 404

    # 若之後要加入留言系統，可以啟用這段
    # comments = CommentModel.get_comments_by_post(post_id)

    return render_template(
        "post_detail.html",
        post=post,
        # comments=comments
    )