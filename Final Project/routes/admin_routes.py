# routes/admin_routes.py

from flask import Blueprint, render_template, request, session, abort, redirect, url_for
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

        SettingsModel.update_settings(
            site_title=site_title,
            subtitle=subtitle,
            footer_text=footer_text,
            about_html=about_html,
            avatar_url=avatar_url,
        )

        # 儲存後留在同一頁
        return redirect(url_for("admin_routes.admin_settings"))

    # GET: 顯示設定頁
    settings = SettingsModel.get_settings()
    return render_template("admin_settings.html", settings=settings)