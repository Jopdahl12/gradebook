from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
assignment = Table('assignment', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=100)),
    Column('total', INTEGER),
    Column('out_of', INTEGER),
    Column('student_id', VARCHAR(length=8)),
    Column('score', FLOAT),
    Column('letter', VARCHAR(length=2)),
    Column('course_name', VARCHAR(length=80)),
)

Assignment = Table('Assignment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('total', Integer, default=ColumnDefault(0)),
    Column('out_of', Integer, default=ColumnDefault(0)),
    Column('student_id', String(length=8)),
    Column('course_name', String(length=80)),
    Column('score', Float, default=ColumnDefault(0.0)),
    Column('letter', String(length=2), default=ColumnDefault('NA')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['assignment'].drop()
    post_meta.tables['Assignment'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['assignment'].create()
    post_meta.tables['Assignment'].drop()
