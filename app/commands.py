import click
from .models import Job, Company, Skill, db


@click.command('print-data')
def print_data():
    print('Job') 
    print(Job.query.all()[:10])
    print()
    print('Company')    
    print(Company.query.all()[:10])
    print()
    print('Skill')
    print(Skill.query.all()[:10])

@click.command('seed-db')
def seed_db():
    skill1 = Skill(
        name='Python'
    )
    skill2 = Skill(
        name='JS'
    )
    company = Company(
        name='visionary company'
    )
    job = Job(
        title='Software engineer',
        yoe_required=1,
        link='fakejobpost.com',
        company=company
    )
    job.skills.append(skill1)
    job.skills.append(skill2)

    db.session.add(company)
    db.session.add(job)
    db.session.add_all([skill1, skill2])
    
    db.session.commit()

@click.command('table-cleanup')
@click.argument("table")
def table_cleanup(table):
    existing_tables = [Job, Company, Skill]
    for existing_table in existing_tables:
        if existing_table.__tablename__ == table:
            existing_table.query.delete()
            db.session.commit()

    

    
    

    
    