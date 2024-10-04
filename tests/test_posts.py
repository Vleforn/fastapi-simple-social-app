from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.Post_w_Vote(**post)
    # Pydantic validation?
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # ToDo assert every post from get method and created posts in test_posts fixture
    assert posts_list[0].Posts.id == test_posts[0].id
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

# get methods for authrorized client are redundant because they're accessable without login
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 200


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200


def test_get_one_post_not_exist(client, test_posts):
    res = client.get("/posts/8888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.Post_w_Vote(**res.json())
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
