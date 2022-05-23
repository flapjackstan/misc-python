from sqlalchemy.orm import Session
from sqlalchemy.orm import close_all_sessions
from sqlalchemy import Table, create_engine
from sqlalchemy import select, MetaData, Column, Float
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base

import config


def core():
    user = config.pg_db.get('user')
    password = config.pg_db.get('password')
    server = config.pg_db.get('server')

    db = 'CamargoDB'

    connection_url = URL.create(drivername="postgresql+psycopg2", username=user, password=password, host=server, database=db)
    engine = create_engine(connection_url, echo=False, future=True)

    # https://docs.sqlalchemy.org/en/14/core/metadata.html
    metadata = MetaData(schema="public")

    table = Table('staging', metadata, 
                  Column('LAT', Float),
                  Column('LON', Float))

    session = Session(engine)

    stmt = select(table).limit(5)

    results_cursor = session.execute(stmt)

    results = results_cursor.all()

    for i in results:
        print(i.LAT, i.LON, i)

    print(results)

    close_all_sessions()

#https://stackoverflow.com/questions/39955521/sqlalchemy-existing-database-query
# https://docs.sqlalchemy.org/en/14/orm/quickstart.html
# https://docs.sqlalchemy.org/en/14/orm/queryguide.html

def orm():
    user = config.pg_db.get('user')
    password = config.pg_db.get('password')
    server = config.pg_db.get('server')

    db = 'CamargoDB'

    connection_url = URL.create(drivername="postgresql+psycopg2", username=user, password=password, host=server, database=db)
    engine = create_engine(connection_url, echo=False, future=True)

    metadata = MetaData(engine, schema="public")
    metadata.reflect(only=['staging'])

    Base = declarative_base()

    class MyClass(Base):
        __table__ = Table('staging', metadata)

        def __repr__(self):
            return f"User(id={self.LAT}, name={self.LON})"

    session = Session(engine)

    stmt = select(MyClass).limit(5)

    ################### METHOD 1 ###################

    # results_cursor = session.execute(stmt)

    # results = results_cursor.scalars()

    # for i in results:
    #     print(i.LAT)

    ################### METHOD 2 ###################

    # i think this would work if it had defined columns
    results_cursor = session.execute(stmt)
    results = results_cursor.scalars().all()

    print(results)

    ################### METHOD 3 ###################

    # for row in session.execute(stmt):
    #     print(row.MyClass.LAT)

    close_all_sessions()

def sqlalchemy_copy():
    user = config.pg_db.get('user')
    password = config.pg_db.get('password')
    server = config.pg_db.get('server')

    db = 'CamargoDB'

    connection_url = URL.create(drivername="postgresql+psycopg2", username=user, password=password, host=server, database=db)
    engine = create_engine(connection_url, echo=False, future=True)



if __name__ == '__main__':
    # works!
    # core()

    # works!
    # orm()

