from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSecurityValidation:
    def test_xss_attempt_in_title(self):
        """Test that XSS attempts in title are blocked"""
        response = client.post(
            "/features/",
            json={"title": "<script>alert('xss')</script>", "desc": "Test"},
        )
        assert response.status_code == 422

    def test_xss_attempt_in_description(self):
        """Test that XSS attempts in description are blocked"""
        response = client.post(
            "/features/",
            json={
                "title": "Test",
                "desc": "<iframe src='javascript:alert(1)'></iframe>",
            },
        )
        assert response.status_code == 422

    def test_sql_injection_attempt(self):
        """Test that SQL injection patterns are blocked"""
        injection_attempts = [
            "test' OR '1'='1",
            "test'; DROP TABLE features; --",
            "test' UNION SELECT * FROM users --",
            "test' AND 1=1 --",
        ]

        for attempt in injection_attempts:
            response = client.post(
                "/features/", json={"title": attempt, "desc": "Test"}
            )
            assert response.status_code == 422, f"SQL injection not blocked: {attempt}"

    def test_title_length_validation(self):
        """Test title length validation"""
        response = client.post(
            "/features/", json={"title": "a" * 101, "desc": "Test description"}
        )
        assert response.status_code == 422

        response = client.post(
            "/features/", json={"title": "", "desc": "Test description"}
        )
        assert response.status_code == 422

    def test_description_length_validation(self):
        """Test description length validation"""
        response = client.post("/features/", json={"title": "Test", "desc": "a" * 501})
        assert response.status_code == 422

    def test_vote_value_validation(self):
        """Test vote value validation"""
        create_resp = client.post(
            "/features/", json={"title": "Test Feature", "desc": "Test Description"}
        )
        feature_id = create_resp.json()["id"]

        response = client.post(f"/features/{feature_id}/vote", json={"value": 0})
        assert response.status_code == 422

        response = client.post(f"/features/{feature_id}/vote", json={"value": 6})
        assert response.status_code == 422

    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = client.get("/health")
        assert response.status_code == 200
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert "X-Frame-Options" in response.headers

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON"""
        response = client.post(
            "/features/",
            data='{"title": "test", "desc": "test"',
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in [400, 422]

    def test_whitespace_only_rejection(self):
        """Test that whitespace-only titles are rejected"""
        response = client.post("/features/", json={"title": "   ", "desc": "Test"})
        assert response.status_code == 422


class TestErrorHandling:
    def test_error_response_safety(self):
        """Test that error responses don't leak internal information"""
        response = client.get("/features/999999")
        assert response.status_code == 404
        error_data = response.json()
        assert "stack_trace" not in error_data
        assert "internal" not in str(error_data).lower()
        assert "error" in error_data
