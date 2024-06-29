from flask import Flask

__version__ = "0.1.0"


def init_app_db(app_inst, db):
    from app.data_helper import DataInitializer
    from app.models import AppRegistryModel

    with app_inst.app_context():
        db.create_all()

        if db.session.execute(
                db.select(AppRegistryModel).filter_by(key='data_inited')
        ).scalar_one_or_none() is None:
            DataInitializer(db.engine).run()
            db.session.add(AppRegistryModel(key='data_inited', value='true'))
            db.session.commit()


def create_app(test_config=None):
    app = Flask(__name__)

    # Configure the app
    app.config.from_object("app.config.AppBaseConfig")
    app.config["API_VERSION"] = __version__

    if test_config:
        app.config.update(test_config)

    # Initialize the extensions
    from app import extensions as ext
    ext.db.init_app(app)
    ext.api.init_app(app)
    ext.jwt.init_app(app)

    # Create the database tables
    init_app_db(app, ext.db)

    # Register the blueprints
    from app.routes import hello_bp, dataset_bp, auth_bp, user_bp
    ext.api.register_blueprint(hello_bp, url_prefix='/api/v1')
    ext.api.register_blueprint(dataset_bp, url_prefix='/api/v1/dataset')
    ext.api.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    ext.api.register_blueprint(user_bp, url_prefix='/api/v1/user')

    return app
