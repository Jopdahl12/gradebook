from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
admin = Table('admin', post_meta,
    Column('id', String(length=8), primary_key=True, nullable=False),
    Column('first_name', String(length=50)),
    Column('last_name', String(length=50)),
    Column('admin_pass', String(length=50)),
)

course = Table('course', post_meta,
    Column('course_num', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
    Column('student_id', String(length=8)),
    Column('admin_id', String(length=8)),
)

student = Table('student', post_meta,
    Column('id', String(length=8), primary_key=True, nullable=False),
    Column('first_name', String(length=50)),
    Column('last_name', String(length=50)),
    Column('GPA', Float),
    Column('year', Integer),
    Column('total_credits', Integer),
    Column('student_pass', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['admin'].create()
    post_meta.tables['course'].create()
    post_meta.tables['student'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['admin'].drop()
    post_meta.tables['course'].drop()
    post_meta.tables['student'].drop()
