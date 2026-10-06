from flask import Blueprint, redirect, render_template, request, url_for

from post_rules import validate_post_input
from repositories.posts import (
    create_post,
    delete_post,
    find_post,
    list_posts,
    update_post,
)


posts_bp = Blueprint("posts", __name__)


def render_not_found(post_id: int):
    return (
        render_template(
            "error.html",
            message=f"{post_id}번 게시글을 찾을 수 없습니다.",
        ),
        404,
    )


@posts_bp.get("/")
def index():
    posts = list_posts()
    return render_template("index.html", posts=posts)


@posts_bp.get("/board/<int:post_id>")
def detail(post_id: int):
    post = find_post(post_id)
    if post is None:
        return render_not_found(post_id)
    return render_template("detail.html", post=post)


@posts_bp.route("/board/new", methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("new.html", title="", body="", error=None)

    title, body, error = validate_post_input(
        request.form.get("title", ""),
        request.form.get("body", ""),
    )
    if error:
        return (
            render_template(
                "new.html",
                title=title,
                body=body,
                error=error,
            ),
            400,
        )

    post = create_post(title, body)
    return redirect(
        url_for("posts.detail", post_id=post["id"]),
        code=303,
    )


@posts_bp.route("/board/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id: int):
    current_post = find_post(post_id)
    if current_post is None:
        return render_not_found(post_id)

    if request.method == "GET":
        return render_template(
            "edit.html",
            post=current_post,
            error=None,
        )

    title, body, error = validate_post_input(
        request.form.get("title", ""),
        request.form.get("body", ""),
    )
    if error:
        return (
            render_template(
                "edit.html",
                post={"id": post_id, "title": title, "body": body},
                error=error,
            ),
            400,
        )

    updated_post = update_post(post_id, title, body)
    if updated_post is None:
        return render_not_found(post_id)

    return redirect(
        url_for("posts.detail", post_id=post_id),
        code=303,
    )


@posts_bp.route("/board/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post_view(post_id: int):
    post = find_post(post_id)
    if post is None:
        return render_not_found(post_id)

    if request.method == "GET":
        return render_template("delete.html", post=post)

    deleted_post = delete_post(post_id)
    if deleted_post is None:
        return render_not_found(post_id)

    return redirect(url_for("posts.index"), code=303)
