import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


def _require_env(name: str) -> str:
	value = os.getenv(name)
	if not value:
		raise RuntimeError(f"Missing required environment variable: {name}")
	return value


def _database_uri() -> str:
	url = os.getenv("DATABASE_URL")
	if url:
		return url

	host = _require_env("DB_HOST")
	port = _require_env("DB_PORT")
	name = _require_env("DB_NAME")
	user = quote_plus(_require_env("DB_USER"))
	password = quote_plus(_require_env("DB_PASSWORD"))
	return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


class Config:
	SQLALCHEMY_DATABASE_URI = _database_uri()
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DB_CONNECT_RETRIES = int(os.getenv("DB_CONNECT_RETRIES", "30"))
	DB_CONNECT_DELAY = float(os.getenv("DB_CONNECT_DELAY", "2"))
	SECRET_KEY = _require_env("SECRET_KEY")