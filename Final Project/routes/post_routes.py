import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, abort, Response
from models.post_model import PostModel
from models.category_model import CategoryModel
from models.comment_model import CommentModel
from models.user_model import UserModel

post_bp = Blueprint("post_routes", __name__)


def _estimate_reading_time(html):
    """粗估閱讀時間（以 220 wpm 近似）"""
    text = re.sub(r"<[^>]+>", " ", html or "")
    words = re.findall(r"\w+", text)
    minutes = max(1, round(len(words) / 220))
    return minutes


# =============================
# 單篇文章頁（含留言）
# =============================
@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = PostModel.get_post_by_id(post_id)
    if not post:
        return render_template("error.html", message="文章不存在"), 404

    comments = CommentModel.get_comments_by_post(post_id)
    reading_time = _estimate_reading_time(post["content"])
    author = UserModel.find_by_id(post["user_id"]) if post.get("user_id") else None

    # 取得前後文章 + 同分類推薦
    all_posts = list(PostModel.get_all_posts())
    prev_post = next_post = None
    related_posts = []

    for idx, p in enumerate(all_posts):
        if p["id"] == post_id:
            if idx + 1 < len(all_posts):
                next_post = all_posts[idx + 1]
            if idx - 1 >= 0:
                prev_post = all_posts[idx - 1]
            break

    related_posts = [
        p for p in all_posts
        if p["category_id"] == post["category_id"] and p["id"] != post_id
    ][:3]

    return render_template(
        "post_detail.html",
        post=post,
        comments=comments,
        reading_time=reading_time,
        author=author,
        prev_post=prev_post,
        next_post=next_post,
        related_posts=related_posts
    )


# =============================
# 作者專頁：顯示該作者文章
# =============================
@post_bp.route("/author/<username>")
def author_page(username):
    user = UserModel.find_by_username(username)
    if not user:
        return render_template("error.html", message="作者不存在"), 404

    page = request.args.get("page", 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page

    posts, total = PostModel.get_posts_by_user_paginated(user["id"], per_page, offset)
    total_pages = max(1, -(-total // per_page))
    return render_template(
        "author_posts.html",
        author=user,
        posts=posts,
        page=page,
        total_pages=total_pages
    )


@post_bp.route("/author/<username>/rss")
def author_rss(username):
    user = UserModel.find_by_username(username)
    if not user:
        abort(404)

    posts = PostModel.get_posts_by_user(user["id"])
    items = []
    for p in posts:
        link = url_for("post_routes.post_detail", post_id=p["id"], _external=True)
        pub_date = p["created_at"]
        items.append(f"""
        <item>
            <title><![CDATA[{p['title']}]]></title>
            <link>{link}</link>
            <guid isPermaLink="false">{p['id']}</guid>
            <pubDate>{pub_date}</pubDate>
            <description><![CDATA[{p['content'][:200]}]]></description>
        </item>
        """)

    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title><![CDATA[{user['username']} - LumenFilm 作者 RSS]]></title>
        <link>{url_for('post_routes.author_page', username=user['username'], _external=True)}</link>
        <description><![CDATA[{user.get('bio') or '作者文章訂閱'}]]></description>
        {''.join(items)}
      </channel>
    </rss>"""
    return Response(feed, content_type="application/rss+xml; charset=utf-8")


# =============================
# 作者列表
# =============================
@post_bp.route("/authors")
def authors_index():
    authors = UserModel.get_all_authors()
    return render_template("authors.html", authors=authors)


# =============================
# 新增文章（Admin Only）
# =============================
@post_bp.route("/new_post", methods=["GET", "POST"])
def new_post():
    if session.get("role") not in ("admin", "author", "developer"):
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
    if session.get("role") not in ("admin", "developer"):
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
    role = session.get("role")
    user_id = session.get("user_id")
    if role not in ("admin", "author", "developer"):
        abort(403)

    post = PostModel.get_post_by_id(post_id)
    if not post:
        return render_template("error.html", message="文章不存在"), 404

    # 作者只能編輯自己的文章
    if role == "author" and post["user_id"] != user_id:
        abort(403)

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
    role = session.get("role")
    user_id = session.get("user_id")
    if role not in ("admin", "author", "developer"):
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

    # 只有作者本人或管理員可以更新
    post = PostModel.get_post_by_id(post_id)
    if role == "author" and post and post["user_id"] != user_id:
        abort(403)

    # 更新 DB
    PostModel.update_post(
        post_id=post_id,
        title=title,
        content=content,
        category_id=category_id_int,
        cover_image_url=cover_image_url
    )

    return redirect(url_for("post_routes.post_detail", post_id=post_id))
