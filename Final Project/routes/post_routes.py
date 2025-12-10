from flask import Blueprint, render_template, request, redirect, url_for, session
from models.post_model import PostModel
from models.category_model import CategoryModel

post_bp = Blueprint("post_routes", __name__)

# ---------------------------
# /new_post（Admin Only）
# ---------------------------
@post_bp.route("/new_post", methods=["GET", "POST"])
def new_post():
    # ---- Admin Only 檢查 ----
    if session.get("role") != "admin":
        return "403 Forbidden：只有管理者能發文", 403

    categories = CategoryModel.get_all_categories()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        category_id = request.form.get("category_id")
        cover_image = request.form.get("cover_image")

        # 確保必填欄位完整
        if not title or not content or not category_id:
            return render_template("new_post.html", 
                                   categories=categories,
                                   error="標題、內容與分類為必填")

        # ---- 寫入資料庫 ----
        new_id = PostModel.create_post(
            title=title,
            content=content,
            category_id=category_id,
            user_id=session["user_id"],
            cover_image_url=cover_image
        )

        # ---- 發文成功 → 導向文章內容頁 ----
        return redirect(url_for("post_routes.post_detail", post_id=new_id))

    # GET：顯示表單
    return render_template("new_post.html", categories=categories)