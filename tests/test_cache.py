import time

from fastapi.testclient import TestClient

from app.core.cache import SimpleCache
from app.main import app

client = TestClient(app)


def test_cache_set_get():
    cache = SimpleCache()
    cache.set("test_key", "test_value", ttl_seconds=10)
    assert cache.get("test_key") == "test_value"
    assert cache.get("non_existent") is None


def test_cache_ttl():
    cache = SimpleCache()
    cache.set("temp_key", "temp_value", ttl_seconds=1)
    assert cache.get("temp_key") == "temp_value"
    time.sleep(1.1)
    assert cache.get("temp_key") is None


def test_cache_invalidation():
    cache = SimpleCache()
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    assert cache.get("key1") == "value1"
    cache.invalidate("key1")
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"


def test_cache_clear():
    cache = SimpleCache()
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None


def test_stats_endpoint_caching():
    response1 = client.get("/features/stats")
    assert response1.status_code == 200
    data1 = response1.json()
    assert not data1["cached"]
    response2 = client.get("/features/stats")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["cached"]
    assert data1["total_features"] == data2["total_features"]
    assert data1["total_votes"] == data2["total_votes"]


def test_cache_invalidation_on_data_change():
    response1 = client.get("/features/stats")
    assert response1.status_code == 200
    client.post("/features/", json={"title": "Test Feature", "desc": "Test"})
    response2 = client.get("/features/stats")
    assert response2.status_code == 200
    data2 = response2.json()
    assert not data2["cached"]
