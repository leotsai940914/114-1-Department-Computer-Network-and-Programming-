from flask import Blueprint, request, redirect, url_for, abort
from models.comment_model import CommentModel

comment_bp = Blueprint("comment_routes", __name__)

@comment_bp.route("/comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):
    nickname = request.form.get("nickname")
    content = request.form.get("content")

    # 必填欄位驗證
    if not nickname or not content:
        # 回到文章頁 + 錯誤訊息（用 query string）
        return redirect(url_for("post_routes.post_detail", 
                                post_id=post_id, 
                                error="留言與暱稱不可為空"))

    # 寫入 DB
    CommentModel.create_comment(
        post_id=post_id,
        nickname=nickname,
        content=content
    )

    # redirect 回該文章頁
    return redirect(url_for("post_routes.post_detail", post_id=post_id))