"""Security headers must be on every response: pages, API and errors."""
import pytest


@pytest.mark.parametrize("path", ["/api/health", "/api/users", "/api/nothing", "/nope.css"])
def test_security_headers_present(client, path):
	res = client.get(path)
	assert res.headers["X-Content-Type-Options"] == "nosniff"
	assert res.headers["X-Frame-Options"] == "DENY"
	csp = res.headers["Content-Security-Policy"]
	assert "default-src 'self'" in csp
	assert "frame-ancestors 'none'" in csp


def test_cors_is_not_enabled(client):
	# Frontend and API share one domain (ingress routes /api), so CORS stays off
	res = client.get("/api/health", headers={"Origin": "https://evil.example"})
	assert "Access-Control-Allow-Origin" not in res.headers
