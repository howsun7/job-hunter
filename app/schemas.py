from marshmallow_sqlalchemy import fields
from .main import ma
from .models import Job, Skill, Company

class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill

class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company
    
class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Job
    
    skills = fields.Nested(SkillSchema, many=True)
    company = fields.Nested(CompanySchema)