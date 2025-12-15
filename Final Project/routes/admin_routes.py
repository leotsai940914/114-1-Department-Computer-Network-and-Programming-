# routes/admin_routes.py

import os
import uuid
from flask import Blueprint, render_template, request, session, abort, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
from models.post_model import PostModel
from models.comment_model import CommentModel
from models.category_model import CategoryModel
from models.settings_model import SettingsModel
from models.user_model import UserModel

admin_bp = Blueprint("admin_routes", __name__)


# ===============================
# Admin Home Dashboard
# ===============================
@admin_bp.route("/admin")
def admin_home():
    if session.get("role") not in ("admin", "developer"):
        abort(403)

    # 所有文章
    posts = PostModel.get_all_posts(include_unpublished=True)
    total_posts = len(posts)

    # 統計數據
    total_comments = CommentModel.count_all()      # 在 CommentModel 中實作
    total_categories = CategoryModel.count_all()   # 在 CategoryModel 中實作
    users = UserModel.get_all_users()

    return render_template(
        "admin_home.html",
        posts=posts,
        total_posts=total_posts,
        total_comments=total_comments,
        total_categories=total_categories,
        users=users,
    )


# ===============================
# 🔧 站點設定頁 /admin/settings
# ===============================
@admin_bp.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    if session.get("role") not in ("admin", "developer"):
        abort(403)

    if request.method == "POST":
        site_title = request.form.get("site_title")
        subtitle = request.form.get("subtitle")
        footer_text = request.form.get("footer_text")
        about_html = request.form.get("about_html")  # About 頁面的 HTML
        avatar_url = request.form.get("avatar_url")
        featured_post_id = request.form.get("featured_post_id") or None
        featured_tagline = request.form.get("featured_tagline") or ""
        author_avatar = request.form.get("author_avatar")
        author_bio = request.form.get("author_bio")

        # 轉型 featured_post_id
        try:
            featured_post_id = int(featured_post_id) if featured_post_id else None
        except ValueError:
            featured_post_id = None

        SettingsModel.update_settings(
            site_title=site_title,
            subtitle=subtitle,
            footer_text=footer_text,
            about_html=about_html,
            avatar_url=avatar_url,
            featured_post_id=featured_post_id,
            featured_tagline=featured_tagline,
        )

        # 更新作者資料
        if session.get("user_id"):
            UserModel.update_profile(
                user_id=session["user_id"],
                avatar_url=author_avatar,
                bio=author_bio
            )

        # 儲存後留在同一頁
        return redirect(url_for("admin_routes.admin_settings"))

    # GET: 顯示設定頁
    settings = SettingsModel.get_settings()
    posts = PostModel.get_all_posts()
    author = UserModel.find_by_id(session.get("user_id")) if session.get("user_id") else None
    return render_template("admin_settings.html", settings=settings, posts=posts, author=author)


# ===============================
# 圖片上傳（Admin Only, About 內文用）
# ===============================
@admin_bp.route("/admin/upload_image", methods=["POST"])
def upload_image():
    if session.get("role") not in ("admin", "developer"):
        abort(403)

    if "file" not in request.files:
        return jsonify({"error": "缺少檔案欄位"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "未選擇檔案"}), 400

    # 副檔名檢查
    allowed = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", set())
    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in allowed:
        return jsonify({"error": "僅允許圖片格式: " + ", ".join(sorted(allowed))}), 400

    # 儲存檔案
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    new_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(upload_dir, new_name)
    # 以 werkzeug 嚴格存檔，並重新檢查副檔名
    try:
        file.save(save_path)
    except Exception:
        return jsonify({"error": "檔案儲存失敗"}), 500

    url = url_for("static", filename=f"uploads/{new_name}", _external=False)
    return jsonify({"url": url})


# ===============================
# 變更使用者角色（Admin Only）
# ===============================
@admin_bp.route("/admin/users/<int:user_id>/role", methods=["POST"])
def update_user_role(user_id):
    if session.get("role") not in ("admin", "developer"):
        abort(403)

    new_role = request.form.get("role")
    if new_role not in ("admin", "author", "visitor", "developer"):
        return abort(400)

    # 保護 Developer 角色不被降級（至少要另一個 admin/developer）
    target = UserModel.find_by_id(user_id)
    if target and target["role"] == "developer" and new_role != "developer":
        return abort(403)

    UserModel.update_role(user_id, new_role)
    return redirect(url_for("admin_routes.admin_home"))


# ===============================
# 調整文章狀態（Admin/Developer）
# ===============================
@admin_bp.route("/admin/posts/<int:post_id>/status", methods=["POST"])
def update_post_status(post_id):
    if session.get("role") not in ("admin", "developer"):
        abort(403)
    status = request.form.get("status")
    if status not in ("draft", "published"):
        abort(400)
    PostModel.update_status(post_id, status)
    return redirect(url_for("admin_routes.admin_home"))
