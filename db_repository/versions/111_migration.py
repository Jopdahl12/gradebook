from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
assignment = Table('assignment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('total', Integer, default=ColumnDefault(0)),
    Column('out_of', Integer, default=ColumnDefault(0)),
    Column('student_id', String(length=8)),
    Column('class_name', String(length=80)),
    Column('score', Float, default=ColumnDefault(0.0)),
    Column('letter', String(length=2), default=ColumnDefault('NA')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['assignment'].columns['class_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['assignment'].columns['class_name'].drop()
