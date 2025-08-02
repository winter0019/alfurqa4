# main.py

import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from firebase_functions import https_fn

# Extensions
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        WTF_CSRF_ENABLED=True,  # Ensure CSRF is enabled
    )
    
    # Initialize Flask extensions
    bcrypt.init_app(app)
    csrf.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

# Flask app instance
app = create_app()

# Firebase Cloud Function entry point
@https_fn.on_request()
def alfurqa_academy_app(req: https_fn.Request) -> https_fn.Response:
    """
    Entrypoint for handling Firebase HTTPS requests using Flask.
    """
    with app.app_context():
        return app.full_dispatch_request()
