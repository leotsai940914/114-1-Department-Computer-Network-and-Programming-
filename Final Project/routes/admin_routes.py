# routes/admin_routes.py

import os
import uuid
from flask import Blueprint, render_template, request, session, abort, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
from models.post_model import PostModel
from models.comment_model import CommentModel
from models.category_model import CategoryModel
from models.settings_model import SettingsModel

admin_bp = Blueprint("admin_routes", __name__)


# ===============================
# Admin Home Dashboard
# ===============================
@admin_bp.route("/admin")
def admin_home():
    if session.get("role") != "admin":
        abort(403)

    # 所有文章
    posts = PostModel.get_all_posts()
    total_posts = len(posts)

    # 統計數據
    total_comments = CommentModel.count_all()      # 在 CommentModel 中實作
    total_categories = CategoryModel.count_all()   # 在 CategoryModel 中實作

    return render_template(
        "admin_home.html",
        posts=posts,
        total_posts=total_posts,
        total_comments=total_comments,
        total_categories=total_categories,
    )


# ===============================
# 🔧 站點設定頁 /admin/settings
# ===============================
@admin_bp.route("/admin/settings", methods=["GET", "POST"])
def admin_settings():
    if session.get("role") != "admin":
        abort(403)

    if request.method == "POST":
        site_title = request.form.get("site_title")
        subtitle = request.form.get("subtitle")
        footer_text = request.form.get("footer_text")
        about_html = request.form.get("about_html")  # About 頁面的 HTML
        avatar_url = request.form.get("avatar_url")
        featured_post_id = request.form.get("featured_post_id") or None
        featured_tagline = request.form.get("featured_tagline") or ""

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

        # 儲存後留在同一頁
        return redirect(url_for("admin_routes.admin_settings"))

    # GET: 顯示設定頁
    settings = SettingsModel.get_settings()
    posts = PostModel.get_all_posts()
    return render_template("admin_settings.html", settings=settings, posts=posts)


# ===============================
# 圖片上傳（Admin Only, About 內文用）
# ===============================
@admin_bp.route("/admin/upload_image", methods=["POST"])
def upload_image():
    if session.get("role") != "admin":
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
    file.save(save_path)

    url = url_for("static", filename=f"uploads/{new_name}", _external=False)
    return jsonify({"url": url})
