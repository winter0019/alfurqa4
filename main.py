# main.py

import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

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

# App instance for Flask CLI and Render
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
