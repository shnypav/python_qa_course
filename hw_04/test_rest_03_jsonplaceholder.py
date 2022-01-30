import pytest
import requests


def test_01_get_posts():
    post_id = 22
    posts = requests.get("https://jsonplaceholder.typicode.com/posts")
    assert posts.status_code == 200

    post = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    result = post.json()
    assert post.status_code == 200
    assert result["id"] == post_id


@pytest.mark.parametrize("req_type, post_id",
                         [("from post", 12), ("from comment", 15)],
                         ids=["Comments for post_id", "Comments filtered by post_id"])
def test_02_get_comments(req_type, post_id):
    if req_type == "from post":
        base_url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    else:
        base_url = f"https://jsonplaceholder.typicode.com/comments?postId={post_id}"

    r = requests.get(base_url)
    result = r.json()

    assert r.status_code == 200

    for row in result:
        assert row["postId"] == post_id


def test_03_new_post():
    base_url = "https://jsonplaceholder.typicode.com/posts"

    headers = {
        "Content-type": "application/json; charset=UTF-8"
    }
    post = {
        "title": "Temp_post",
        "body": "Post_body",
        "userId": 66
    }

    r = requests.post(base_url, json=post, headers=headers)
    assert r.status_code == 201


def test_04_delete():
    post_id = 33
    d = requests.delete(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    assert d.status_code == 200


@pytest.mark.parametrize("user_id, posts_qty", [(5, 4), (4, 4)])
def test_05_posts_by_user(user_id, posts_qty):
    r = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}/posts")
    result = r.json()
    assert r.status_code == 200
    assert len(result[0]) == posts_qty
