from flask import Blueprint, render_template

post_bp = Blueprint("post_routes", __name__)

@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    return render_template("post_detail.html")

@post_bp.route("/new_post")
def new_post():
    return render_template("new_post.html")