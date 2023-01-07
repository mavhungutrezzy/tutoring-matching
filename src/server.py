import logging
import os

from flasgger import Swagger
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from http import HTTPStatus

import routes
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from database import db


def create_app():

    app = Flask(__name__)

    if os.environ.get("WORK_ENV") == "PROD":
        config = ProductionConfig
    elif os.environ.get("WORK_ENV") == "TEST":
        config = TestingConfig
    else:
        config = DevelopmentConfig

    app.config.from_object(config)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://mavhungu:password@localhost:5432/tutoring"

    db.init_app(app)
    Migrate(app, db)
    Swagger(app)
    JWTManager(app)

    app.register_blueprint(routes.user.USER_BLUEPRINT)

    with app.app_context():
        db.create_all()

    app.config["SWAGGER"] = {
        "swagger_version": "2.0",
        "title": "Application",
        "specs": [
            {
                "version": "0.0.1",
                "title": "Application",
                "endpoint": "spec",
                "route": "/application/spec",
                "rule_filter": lambda rule: True,  # all in
            }
        ],
        "static_url_path": "/apidocs",
    }

    logging.basicConfig(
        filename="server.log",
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
    )

    @app.errorhandler(400)
    def bad_request(error):
        logging.error(error)
        return jsonify(
            {
                "success": False,
                "message": "Validation errors or missing input data",
                "error": str(error),
            },
        )

    @app.errorhandler(404)
    def not_found(error):
        logging.error(error)
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Resource method is not available",
                    "error": str(error),
                }
            ),
            HTTPStatus.NOT_FOUND,
        )

    @app.errorhandler(500)
    def server_error(error):
        logging.error(error)
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Server threw some exceptions while running the method",
                    "error": str(error),
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        logging.error(error)
        return (
            jsonify(
                {
                    "success": False,
                    "message": "The method is not allowed for the requested URL",
                    "error": str(error),
                }
            ),
            HTTPStatus.METHOD_NOT_ALLOWED,
        )

    @app.errorhandler(502)
    def method_not_allowed(error):
        logging.error(error)
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Server was not able to get the response from another upstream server",
                    "error": str(error),
                }
            ),
            HTTPStatus.BAD_GATEWAY,
        )

    return app


if __name__ == "__main__":
    create_app().run()
