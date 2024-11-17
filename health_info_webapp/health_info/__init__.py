from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from health_info.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from health_info.main.routes import main
    app.register_blueprint(main)

    from health_info.users.routes import users
    app.register_blueprint(users)

    from health_info.patients.routes import patients
    app.register_blueprint(patients)

    from health_info.disease import disease
    app.register_blueprint(disease)

    from health_info.doctor import doctor
    app.register_blueprint(doctor)

    from health_info.public_servant import public_servant
    app.register_blueprint(public_servant)

    from health_info.record import record
    app.register_blueprint(record)

    from health_info.discover import discover
    app.register_blueprint(discover)

    from health_info.patient_disease import patient_disease
    app.register_blueprint(patient_disease)

    from health_info.country import country
    app.register_blueprint(country)

    from health_info.disease_type import disease_type
    app.register_blueprint(disease_type)

    from health_info.specialize import specialize
    app.register_blueprint(specialize)

    return app