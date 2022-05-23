from sqlalchemy.orm import Session, close_all_sessions
from sqlalchemy import create_engine, MetaData, Table, Column, Float, select, text, Integer, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL

import config


def core_read():
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
def orm_read_table():
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

        # need to add the rest of cols
        def __repr__(self):
            return f"Address(LAT={self.LAT}, LON={self.LON})"

    session = Session(engine)

    stmt = select(MyClass).limit(5)

    results_cursor = session.execute(stmt)
    results = results_cursor.scalars().all()

    print(results, type(results))

    close_all_sessions()


def orm_create_table():
    user = config.pg_db.get('user')
    password = config.pg_db.get('password')
    server = config.pg_db.get('server')

    db = 'CamargoDB'

    connection_url = URL.create(drivername="postgresql+psycopg2", username=user, password=password, host=server, database=db)
    engine = create_engine(connection_url, echo=False)

    metadata = MetaData(engine, schema="public")

    Base = declarative_base(metadata=metadata)

    class Simpsons(Base):
        __tablename__ = 'simpsons'
        id = Column(Integer, primary_key=True)
        name = Column(String(20))
        street = Column(Text())

        # need to add the rest of cols
        def __repr__(self):
            return f"Simpson(id={self.id}, name={self.name}, street={self.street})"

    Base.metadata.create_all(engine)

    close_all_sessions()


def sqlalchemy_copy():
    user = config.pg_db.get('user')
    password = config.pg_db.get('password')
    server = config.pg_db.get('server')

    db = 'CamargoDB'

    connection_url = URL.create(drivername="postgresql+psycopg2", username=user, password=password, host=server, database=db)
    engine = create_engine(connection_url, echo=False)

    connection = engine.connect().connection

    # get a cursor on that connection
    cursor = connection.cursor()

    copy_from = """
                COPY simpsons 
                FROM STDIN
                WITH (
                    FORMAT CSV,
                    DELIMITER ',',
                    HEADER
                );
                """

    # running the copy statement
    with open('../data/simpsons_addresses.csv') as f:
        cursor.copy_expert(copy_from, file=f)

    # don't forget to commit the changes.
    connection.commit()

    close_all_sessions()


def temp_table_copy_upsert():
    user = config.pg_db.get('user')
    password = config.pg_db.get('password')
    server = config.pg_db.get('server')

    db = 'CamargoDB'

    connection_url = URL.create(drivername="postgresql+psycopg2", username=user, password=password, host=server, database=db)
    engine = create_engine(connection_url, echo=False)

    connection = engine.connect().connection

    # get a cursor on that connection
    cursor = connection.cursor()

    cursor.execute("create TEMP TABLE temp_simpsons(id int primary key, name text, street text);")

    copy_from = """
                COPY temp_simpsons 
                FROM STDIN
                WITH (
                    FORMAT CSV,
                    DELIMITER ',',
                    HEADER
                );
                """

    # running the copy statement
    with open('../data/simpsons_addresses_address_id_update.csv') as f:
        cursor.copy_expert(copy_from, file=f)

    cursor.execute('''insert into simpsons
        (SELECT "id", "name", "street" from 
                    (select "id", "name", "street" from temp_simpsons
                         where not exists
                        (select * from simpsons where temp_simpsons."id" = simpsons."id")
                        or NOT EXISTS
                        (select * from simpsons where temp_simpsons."street" = simpsons."street")
                    ) as subtable
        )
        on conflict (id) do update SET "street" = excluded."street";''')

    connection.commit()

    connection.close()
