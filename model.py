from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import sqlite3

ENGINE = create_engine("sqlite:///rack.db", echo=False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = session.query_property()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
