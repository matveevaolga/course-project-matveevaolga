from fastapi.testclient import TestClient

from app.features.store import feat_store
from app.main import app

client = TestClient(app)


def test_create_feat():
    resp = client.post("/features/", json={"title": "New Feature", "desc": "Test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New Feature"
    assert data["votes_count"] == 0


def test_vote_for_feat():
    feat_resp = client.post("/features/", json={"title": "Vote Test", "desc": "Test"})
    feat_id = feat_resp.json()["id"]

    vote_resp = client.post(f"/features/{feat_id}/vote", json={"value": 1})
    assert vote_resp.status_code == 200

    feat_after = client.get(f"/features/{feat_id}").json()
    assert feat_after["votes_count"] == 1


def test_get_top_feats():
    resp = client.get("/features/top")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_feature_votes_workflow():
    create_resp = client.post(
        "/features/", json={"title": "some feature", "desc": "some feature"}
    )
    assert create_resp.status_code == 200
    feature_id = create_resp.json()["id"]

    vote_resp = client.post(f"/features/{feature_id}/vote", json={"value": 1})
    assert vote_resp.status_code == 200

    top_resp = client.get("/features/top")
    assert top_resp.status_code == 200
    assert len(top_resp.json()) > 0


def test_features_stats_empty():
    feat_store.reset_for_tests()

    response = client.get("/features/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_features"] == 0
    assert data["total_votes"] == 0
    assert data["total_vote_value"] == 0
    assert data["avg_votes_per_feature"] == 0
    assert data["most_voted_feature"] is None


def test_features_stats_with_data():
    feat_store.reset_for_tests()

    client.post("/features/", json={"title": "Feature 1", "desc": "Test feature 1"})
    client.post("/features/", json={"title": "Feature 2", "desc": "Test feature 2"})

    client.post("/features/1/vote", json={"value": 1})
    client.post("/features/1/vote", json={"value": 1})
    client.post("/features/2/vote", json={"value": -1})

    response = client.get("/features/stats")
    assert response.status_code == 200
    data = response.json()

    assert data["total_features"] == 2
    assert data["total_votes"] == 3
    assert data["total_vote_value"] == 1
    assert data["avg_votes_per_feature"] == 1.5
    assert data["most_voted_feature"]["id"] == 1
    assert data["most_voted_feature"]["votes_count"] == 2
