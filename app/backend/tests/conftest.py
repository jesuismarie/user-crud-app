"""Shared pytest setup. pytest loads this file automatically."""
import pytest
from app import create_app, db


class TestingConfig:
	"""In-memory SQLite. No MySQL and no .env required."""
	TESTING = True
	PROPAGATE_EXCEPTIONS = False
	SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = "test-only-key"
	DB_CONNECT_RETRIES = 1
	DB_CONNECT_DELAY = 0


@pytest.fixture
def app(tmp_path):
	(tmp_path / "secret.txt").write_text("outside")

	application = create_app(TestingConfig)
	yield application
	with application.app_context():
		db.session.remove()
		db.drop_all()


@pytest.fixture
def client(app):
	return app.test_client()
