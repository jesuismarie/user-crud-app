import time
from sqlalchemy.exc import OperationalError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _init_db(app):
	"""Create tables, retrying while the database is still starting."""
	retries = app.config["DB_CONNECT_RETRIES"]
	for attempt in range(1, retries + 1):
		try:
			db.create_all()
			return
		except OperationalError as exc:
			if attempt == retries:
				raise
			app.logger.warning("Database not ready (%s/%s): %s", attempt, retries, exc.orig)
			time.sleep(app.config["DB_CONNECT_DELAY"])


def create_app(config_class=None):
	if config_class is None:
		from .config import Config
		config_class = Config
	app = Flask(__name__, static_folder=None)
	app.config.from_object(config_class)

	db.init_app(app)

	from .routes import api_bp
	app.register_blueprint(api_bp)

	@app.after_request
	def add_security_headers(response):
		response.headers["X-Content-Type-Options"] = "nosniff"
		response.headers["X-Frame-Options"] = "DENY"
		response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
		return response

	with app.app_context():
		_init_db(app)

	return app
