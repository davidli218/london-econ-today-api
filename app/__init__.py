from flask import Flask

__version__ = "0.1.0"


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

    # Register the API routes
    from app.routes import register_blueprints
    register_blueprints(ext.api)

    # Create the database tables
    with app.app_context():
        ext.db.create_all()

        from app.data_helper import DataInitializer
        from app.models import AppRegistryModel

        if ext.db.session.execute(
                ext.db.select(AppRegistryModel).filter_by(key='data_inited')
        ).scalar_one_or_none() is None:
            DataInitializer(ext.db.engine).run()
            ext.db.session.add(AppRegistryModel(key='data_inited', value='true'))
            ext.db.session.commit()

    return app
