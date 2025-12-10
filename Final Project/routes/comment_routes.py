from flask import Blueprint

comment_bp = Blueprint("comment_routes", __name__)

@comment_bp.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):
    return f"留言功能之後實作：來自 post {post_id}"