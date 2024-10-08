from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Import and register the routes
        from .routes import init_routes
        init_routes(app)

    return app
