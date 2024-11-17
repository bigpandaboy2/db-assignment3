from datetime import date
from health_info import db

class Country(db.Model):
    __tablename__ = 'country'
    cname = db.Column(db.String(50), primary_key=True)
    population = db.Column(db.BigInteger)

    users = db.relationship('Users', backref='country', lazy=True)
    records = db.relationship(
        'Record',
        back_populates='country',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    discoveries = db.relationship(
        'Discover',
        back_populates='country',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Users(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(40))
    salary = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    cname = db.Column(db.String(50), db.ForeignKey('country.cname'))

    patient = db.relationship(
        'Patients',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    public_servant = db.relationship(
        'PublicServant',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    doctor = db.relationship(
        'Doctor',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Patients(db.Model):
    __tablename__ = 'patients'
    email = db.Column(
        db.String(60),
        db.ForeignKey('users.email', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )

    user = db.relationship('Users', back_populates='patient', uselist=False)
    patient_diseases = db.relationship(
        'PatientDisease',
        back_populates='patient',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class DiseaseType(db.Model):
    __tablename__ = 'disease_type'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))

    specializations = db.relationship('Specialize', back_populates='disease_type')
    diseases = db.relationship(
        'Disease',
        back_populates='disease_type',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    specializes = db.relationship(
        'Specialize',
        back_populates='disease_type',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Disease(db.Model):
    __tablename__ = 'disease'
    disease_code = db.Column(db.String(50), primary_key=True)
    pathogen = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(140))
    id = db.Column(
        db.Integer,
        db.ForeignKey('disease_type.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False
    )

    disease_type = db.relationship('DiseaseType', back_populates='diseases')
    records = db.relationship(
        'Record',
        back_populates='disease',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    discoveries = db.relationship(
        'Discover',
        back_populates='disease',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    patient_diseases = db.relationship(
        'PatientDisease',
        back_populates='disease',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Discover(db.Model):
    __tablename__ = 'discover'
    cname = db.Column(
        db.String(50),
        db.ForeignKey('country.cname', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    disease_code = db.Column(
        db.String(50),
        db.ForeignKey('disease.disease_code', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    first_enc_date = db.Column(db.Date, nullable=False)

    country = db.relationship('Country', back_populates='discoveries')
    disease = db.relationship('Disease', back_populates='discoveries')

class PublicServant(db.Model):
    __tablename__ = 'public_servant'
    email = db.Column(
        db.String(60),
        db.ForeignKey('users.email', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    department = db.Column(db.String(50), nullable=False)

    user = db.relationship('Users', back_populates='public_servant', uselist=False)
    records = db.relationship(
        'Record',
        back_populates='public_servant',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

class Doctor(db.Model):
    __tablename__ = 'doctor'
    email = db.Column(
        db.String(60),
        db.ForeignKey('users.email', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    degree = db.Column(db.String(20), nullable=False)

    user = db.relationship('Users', back_populates='doctor', uselist=False)
    specializations = db.relationship(
        'Specialize',
        back_populates='doctor',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    specializes = db.relationship(
    'Specialize',
    back_populates='doctor',
    cascade='all, delete-orphan',
    passive_deletes=True
)

class Specialize(db.Model):
    __tablename__ = 'specialize'
    id = db.Column(
        db.Integer,
        db.ForeignKey('disease_type.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    email = db.Column(
        db.String(60),
        db.ForeignKey('doctor.email', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )

    doctor = db.relationship('Doctor', back_populates='specializations')
    disease_type = db.relationship('DiseaseType', back_populates='specializes')


class Record(db.Model):
    __tablename__ = 'record'
    email = db.Column(
        db.String(60),
        db.ForeignKey('public_servant.email', ondelete='CASCADE'),
        primary_key=True
    )
    cname = db.Column(
        db.String(50),
        db.ForeignKey('country.cname', ondelete='CASCADE'),
        primary_key=True
    )
    disease_code = db.Column(
        db.String(50),
        db.ForeignKey('disease.disease_code', ondelete='CASCADE'),
        primary_key=True
    )
    total_deaths = db.Column(db.Integer)
    total_patients = db.Column(db.Integer)

    public_servant = db.relationship('PublicServant', back_populates='records')
    country = db.relationship('Country', back_populates='records')
    disease = db.relationship('Disease', back_populates='records')

class PatientDisease(db.Model):
    __tablename__ = 'patient_disease'
    email = db.Column(
        db.String(60),
        db.ForeignKey('patients.email', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )
    disease_code = db.Column(
        db.String(50),
        db.ForeignKey('disease.disease_code', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    )

    patient = db.relationship('Patients', back_populates='patient_diseases')
    disease = db.relationship('Disease', back_populates='patient_diseases')