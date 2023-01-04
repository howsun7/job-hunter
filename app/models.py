from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import types

db = SQLAlchemy()

job_skill = db.Table(
    'job_skill',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)


class GetOrCreateMixin:
    __table_args__ = {'extend_existing': True}

    @classmethod
    def get_or_create(cls, **kwargs):
        """
        Return an model object (instance).

        Check if a particular model object exists in the model. If the model object 
        exists, return that object; if not, create an model object and return it.
        """

        try:
            instance = cls.get_instance(**kwargs)
        except NoResultFound:
            instance = cls.create_instance(**kwargs)

        return instance

    @classmethod 
    def create_instance(cls, **kwargs):
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
        except Exception:
            raise

        try: 
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise 
        
        return instance

    @classmethod
    def get_instance(cls, **kwargs):
        try:
            instance = cls.query.filter_by(**kwargs).first()
        except InvalidRequestError:
            raise ValueError("property for {} does not exist".format(cls))
        except Exception:
            raise

        if instance is None:
            raise NoResultFound

        return instance
        
class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Job(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(types.url.URLType)
    yoe_required = db.Column(db.Integer, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    skills = db.relationship('Skill', secondary=job_skill, backref='jobs')

    def __repr__(self):
        return f'{self.id}: {self.title}'

class Skill(GetOrCreateMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.name

class Company(GetOrCreateMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    jobs = db.relationship('Job', backref='company')
    
    def __repr__(self):
        return self.name

