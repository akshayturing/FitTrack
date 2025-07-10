from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import config
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

ma = Marshmallow()
# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    # Setup LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify the login view route
    login_manager.login_message = 'Please log in to access this page'
    login_manager.login_message_category = 'info'
    
    # Create tables within application context if they don't exist
    with app.app_context():
        db.create_all()
        # Set up JWT error handlers and callbacks
    from app.auth.jwt_callbacks import register_jwt_callbacks
    register_jwt_callbacks(jwt)
    
    
    # Register blueprints
    from app.routes.user_routes import user_bp
    from app.routes.workout_routes import workout_bp
    from app.auth.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp 
    from app.routes.assignment_routes import assignment_bp
    from app.routes.session_log_routes import session_log_bp
    from app.routes.dashboard_routes import dashboard_bp  # Import dashboard blueprint

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(workout_bp, url_prefix='/api/workouts')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Add this
    app.register_blueprint(assignment_bp, url_prefix='/api/assignments')
    app.register_blueprint(session_log_bp, url_prefix='/api/session-logs')
    app.register_blueprint(dashboard_bp)  # Register without prefix to include UI routes


    return app
    # # Register blueprints
    # from app.routes.user_routes import user_bp
    # from app.routes.workout_routes import workout_bp
    # from app.routes.auth_routes import auth_bp
    
    # app.register_blueprint(user_bp, url_prefix='/api/users')
    # app.register_blueprint(workout_bp, url_prefix='/api/workouts')
    # app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # # Setup JWT error handlers
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_payload):
    #     return {
    #         'status': 401,
    #         'sub_status': 42,
    #         'message': 'The token has expired'
    #     }, 401

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return {
    #         'status': 401,
    #         'sub_status': 43,
    #         'message': 'Signature verification failed'
    #     }, 401

    # @jwt.unauthorized_loader
    # def missing_token_callback(error):
    #     return {
    #         'status': 401,
    #         'sub_status': 44,
    #         'message': 'Request does not contain an access token'
    #     }, 401
        
    # # Create a simple token blacklist
    # # In a production environment, you'd want to use Redis or another cache
    # app.blacklisted_tokens = set()
    
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blacklist(jwt_header, jwt_payload):
    #     jti = jwt_payload['jti']
    #     return jti in app.blacklisted_tokens
    
    # return app

