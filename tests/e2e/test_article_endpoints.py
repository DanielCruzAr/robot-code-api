from tests.conftest import client


def test_post_article(client):
    payload = {
        "title": "Test Article",
        "author": "John Doe",
        "body": "This is a test article.",
        "tags": ["test", "sample"]
    }
    response = client.post("/articles/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert data["body"] == payload["body"]
    assert set(data["tags"]) == set(payload["tags"])


def test_get_articles(client):
    response = client.get("/articles/?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert "total" in data
    assert isinstance(data["articles"], list)


def test_get_article(client):
    # Create article first
    payload = {
        "title": "Get Single Article",
        "author": "Jane Doe",
        "body": "Single article body.",
        "tags": ["single"]
    }
    post_resp = client.post("/articles/", json=payload)
    article_id = post_resp.json()["id"]

    # Get article
    response = client.get(f"/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == article_id
    assert data["title"] == payload["title"]


def test_update_article(client):
    # Create article
    payload = {
        "title": "Update Me",
        "author": "Updater",
        "body": "Old body.",
        "tags": ["old"]
    }
    post_resp = client.post("/articles/", json=payload)
    article_id = post_resp.json()["id"]

    # Update article
    update_payload = {
        "body": "Updated body.",
        "tags": ["updated"]
    }
    response = client.put(f"/articles/{article_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["body"] == update_payload["body"]
    assert set(data["tags"]) == set(update_payload["tags"])


def test_delete_article(client):
    # Create article
    payload = {
        "title": "Delete Me",
        "author": "Deleter",
        "body": "To be deleted.",
        "tags": ["delete"]
    }
    post_resp = client.post("/articles/", json=payload)
    article_id = post_resp.json()["id"]

    # Delete article
    response = client.delete(f"/articles/{article_id}")
    assert response.status_code == 204

    # Try to get deleted article
    get_resp = client.get(f"/articles/{article_id}")
    assert get_resp.status_code == 404
    