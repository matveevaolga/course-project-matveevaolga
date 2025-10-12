from fastapi.testclient import TestClient

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
