from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import types

db = SQLAlchemy()

job_skill = db.Table(
    'job_skill',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

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

class Skill(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.name

class Company(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    jobs = db.relationship('Job', backref='company')
    
    def __repr__(self):
        return self.name

