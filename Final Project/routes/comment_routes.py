from flask import Blueprint, request, redirect, url_for, abort
from models.comment_model import CommentModel
from models.post_model import PostModel

comment_bp = Blueprint("comment_routes", __name__)

@comment_bp.route("/comment/<int:post_id>", methods=["POST"])
def add_comment(post_id):

    # 確認文章存在
    post = PostModel.get_post_by_id(post_id)
    if not post:
        return abort(404)

    nickname = request.form.get("nickname", "").strip()
    content = request.form.get("content", "").strip()

    # 驗證欄位
    if not nickname or not content:
        return redirect(
            url_for("post_routes.post_detail", 
                    post_id=post_id, 
                    error="暱稱與留言內容不得為空")
        )

    # 寫入 DB
    CommentModel.create_comment(
        post_id=post_id,
        nickname=nickname,
        content=content
    )

    return redirect(url_for("post_routes.post_detail", post_id=post_id))