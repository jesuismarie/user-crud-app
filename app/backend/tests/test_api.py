"""API tests. From app/backend run: pytest -v"""
import pytest
from sqlalchemy.exc import OperationalError

from app import db

VALID_USER = {
	"first_name": "Alice",
	"last_name": "Smith",
	"age": 28,
	"email": "alice@example.com",
}


def post_user(client, **overrides):
	return client.post("/api/users", json={**VALID_USER, **overrides})


# --- create ---

def test_create_user_returns_201(client):
	res = post_user(client)
	assert res.status_code == 201
	data = res.get_json()
	assert data["id"] == 1
	assert data["first_name"] == "Alice"
	assert data["last_name"] == "Smith"
	assert data["age"] == 28
	assert data["email"] == "alice@example.com"


def test_create_trims_names_and_lowercases_email(client):
	res = post_user(client, first_name="  Alice  ", last_name="  Smith  ", email="Alice@Example.COM")
	assert res.status_code == 201
	body = res.get_json()
	assert body["first_name"] == "Alice"
	assert body["last_name"] == "Smith"
	assert body["email"] == "alice@example.com"


def test_create_duplicate_email_returns_409(client):
	post_user(client)
	res = post_user(client, first_name="Other")
	assert res.status_code == 409
	assert "already exists" in res.get_json()["error"]


def test_create_duplicate_email_is_case_insensitive(client):
	post_user(client)
	res = post_user(client, email="ALICE@example.com")
	assert res.status_code == 409


def test_create_ignores_unknown_json_fields(client):
	res = client.post("/api/users", json={**VALID_USER, "admin": True})
	assert res.status_code == 201
	assert "admin" not in res.get_json()


# --- read ---

def test_list_users_empty(client):
	res = client.get("/api/users")
	assert res.status_code == 200
	assert res.get_json() == []


def test_list_users_in_id_order(client):
	post_user(client)
	post_user(client, first_name="Bob", email="bob@example.com")
	names = [u["first_name"] for u in client.get("/api/users").get_json()]
	assert names == ["Alice", "Bob"]


def test_get_one_user(client):
	post_user(client)
	res = client.get("/api/users/1")
	assert res.status_code == 200
	assert res.get_json()["email"] == "alice@example.com"


def test_get_unknown_user_returns_json_404(client):
	res = client.get("/api/users/999")
	assert res.status_code == 404
	assert res.is_json
	assert "error" in res.get_json()


# --- update ---

def test_update_age_keeps_other_fields(client):
	post_user(client)
	res = client.put("/api/users/1", json={"age": 29})
	assert res.status_code == 200
	data = res.get_json()
	assert data["age"] == 29
	assert data["first_name"] == "Alice"
	assert data["email"] == "alice@example.com"


def test_update_email_conflict_returns_409(client):
	post_user(client)
	post_user(client, first_name="Bob", email="bob@example.com")
	res = client.put("/api/users/2", json={"email": "alice@example.com"})
	assert res.status_code == 409


def test_update_own_email_is_allowed(client):
	post_user(client)
	res = client.put("/api/users/1", json={"email": "ALICE@example.com"})
	assert res.status_code == 200
	assert res.get_json()["email"] == "alice@example.com"


def test_update_unknown_user_returns_404(client):
	res = client.put("/api/users/999", json={"age": 30})
	assert res.status_code == 404


def test_update_invalid_age_does_not_change_row(client):
	post_user(client)
	res = client.put("/api/users/1", json={"age": "old"})
	assert res.status_code == 400
	assert client.get("/api/users/1").get_json()["age"] == 28


def test_update_without_body_returns_400(client):
	post_user(client)
	res = client.put("/api/users/1", json={})
	assert res.status_code == 400


# --- delete ---

def test_delete_user_then_it_is_gone(client):
	post_user(client)
	res = client.delete("/api/users/1")
	assert res.status_code == 200
	assert "deleted" in res.get_json()["message"]
	assert client.get("/api/users/1").status_code == 404
	assert client.get("/api/users").get_json() == []


def test_delete_unknown_user_returns_404(client):
	assert client.delete("/api/users/999").status_code == 404


# --- validation ---

@pytest.mark.parametrize("field", ["first_name", "last_name", "age", "email"])
def test_create_missing_field_returns_400(client, field):
	payload = {k: v for k, v in VALID_USER.items() if k != field}
	res = client.post("/api/users", json=payload)
	assert res.status_code == 400
	assert field in res.get_json()["error"]


@pytest.mark.parametrize(
	"field, value",
	[
		("first_name", 5),
		("first_name", ""),
		("first_name", "   "),
		("first_name", "x" * 101),
		("last_name", "x" * 101),
		("age", "30"),
		("age", True),
		("age", 1.5),
		("age", -1),
		("age", 151),
		("email", "nope"),
		("email", "a@b"),
		("email", "x" * 150 + "@example.com"),
	],
)
def test_create_rejects_invalid_values(client, field, value):
	res = post_user(client, **{field: value})
	assert res.status_code == 400
	assert res.is_json
	assert client.get("/api/users").get_json() == []


@pytest.mark.parametrize("age", [0, 150])
def test_create_accepts_age_boundaries(client, age):
	assert post_user(client, age=age, email=f"user{age}@example.com").status_code == 201


def test_create_broken_json_returns_400(client):
	res = client.post("/api/users", data="{not json", content_type="application/json")
	assert res.status_code == 400
	assert res.is_json


def test_create_json_list_returns_400(client):
	res = client.post("/api/users", json=[1, 2, 3])
	assert res.status_code == 400


# --- probes ---

def test_health_returns_200(client):
	res = client.get("/api/health")
	assert res.status_code == 200
	assert res.get_json()["status"] == "healthy"


def test_ready_returns_200_when_db_works(client):
	res = client.get("/api/ready")
	assert res.status_code == 200
	assert res.get_json()["status"] == "ready"


def test_ready_returns_503_when_db_is_down(client, monkeypatch):
	def broken(*args, **kwargs):
		raise OperationalError("SELECT 1", {}, Exception("down"))

	monkeypatch.setattr(db.session, "execute", broken)
	res = client.get("/api/ready")
	assert res.status_code == 503
	assert res.get_json()["status"] == "not ready"


def test_health_still_ok_when_db_is_down(client, monkeypatch):
	def broken(*args, **kwargs):
		raise OperationalError("SELECT 1", {}, Exception("down"))

	monkeypatch.setattr(db.session, "execute", broken)
	assert client.get("/api/health").status_code == 200


# --- errors are JSON ---

def test_unknown_url_returns_json_404(client):
	res = client.get("/api/does-not-exist")
	assert res.status_code == 404
	assert res.is_json


def test_wrong_method_returns_json_405(client):
	res = client.delete("/api/health")
	assert res.status_code == 405
	assert res.is_json


# --- unknown paths and traversal ---

def test_missing_frontend_file_returns_json_404(client):
	res = client.get("/nope.css")
	assert res.status_code == 404
	assert res.is_json


def test_path_traversal_does_not_leak_files(client):
	for path in ("/../secret.txt", "/%2e%2e/secret.txt", "/..%2fsecret.txt"):
		res = client.get(path)
		assert res.status_code == 404
		assert b"outside" not in res.data
