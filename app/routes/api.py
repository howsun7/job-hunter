from flask import Blueprint
from app.schemas import JobSchema
from app.models import Job, Company, Skill


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('jobs', methods=['GET'])
def jobs_list():
    schema = JobSchema(many=True)
    jobs = Job.query.all()
    return schema.dump(jobs)

