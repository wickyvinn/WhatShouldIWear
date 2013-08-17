from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey, Table, or_
import psycopg2

ENGINE = create_engine("postgresql+psycopg2:///rack")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
session = Session()

Base = declarative_base()
Base.query = Session.query_property()

class Garment(Base):
	__tablename__ = "garments"
	id = Column(Integer, primary_key = True)
	keywords = Column(String(32), nullable = False)
	type = Column(String(10), nullable = False)

	tag = relationship("Garment_Tag", backref = "parent", cascade="all, delete, delete-orphan")
	search = relationship("Garment_Search", backref = "parent", cascade="all, delete, delete-orphan")
	activity = relationship("Garment_Activity", backref = "parent", cascade="all, delete, delete-orphan")

class Tag(Base):
	__tablename__ = 'tags'
	id = Column(Integer, primary_key = True)
	style = Column(String(32), nullable = False)

class Garment_Tag(Base):
	__tablename__ = "garment_tags"
	id = Column(Integer, primary_key = True)
	garment_id = Column(Integer, ForeignKey("garments.id"))
	tag_id = Column(Integer, ForeignKey("tags.id"))

	tag = relationship("Tag", backref = "parent_assocs")

class Search(Base):
	__tablename__ = "searches"
	id = Column(Integer, primary_key = True)
	url = Column(String(300), nullable = True)
	title = Column(String(200), nullable = True)
	companyname = Column(String(48), nullable = True)
	img = Column(String(300), nullable = True)
	price = Column(String(20), nullable = True)
	thing_id = Column(Integer, nullable = True)
	description = Column(String(400), nullable = True)
	color = Column(String(10), nullable = True)
	primary = Column(Integer, nullable = False)

class Garment_Search(Base):
	__tablename__ = "garment_searches"
	id = Column(Integer, primary_key = True)
	garment_id = Column(Integer, ForeignKey("garments.id"))
	search_id = Column(Integer, ForeignKey("searches.id"))
	search = relationship("Search", backref="parent_assocs")

class Activity(Base):
	__tablename__ = "activities"
	id = Column(Integer, primary_key = True)
	activity = Column(String(32), nullable = False)

class Garment_Activity(Base):
	__tablename__ = "garment_activities"
	id = Column(Integer, primary_key = True)
	garment_id = Column(Integer, ForeignKey("garments.id"))
	activity_id = Column(Integer, ForeignKey("activities.id"))

	activity = relationship("Activity", backref = "parent_assocs")

class Color_Scheme(Base):
	__tablename__ = "color_schemes"
	id = Column(Integer, primary_key = True)
	color1 = Column(String(10), nullable = False)
	color2 = Column(String(10), nullable = True)
	color3 = Column(String(10), nullable = True)
	color4 = Column(String(10), nullable = True)
	color5 = Column(String(10), nullable = True)
	color6 = Column(String(10), nullable = True)

def search_garment_tables():
	Search.__table__
	Garment_Search.__table__
	Base.metadata.create_all(ENGINE)
	print "garment_search and search table created."

def make_garments_table():
	Garment.__table__
	Base.metadata.create_all(ENGINE)
	print "garments table created."

def make_tags_table():
	Tag.__table__
	Base.metadata.create_all(ENGINE)
	print "tags table created."

def make_garment_tags_table():
	Garment_Tag.__table__
	Base.metadata.create_all(ENGINE)
	print "garment_tags table created."

def make_all_tables():
	Garment.__table__
	Tag.__table__
	Garment_Tag.__table__
	Search.__table__
	Garment_Search.__table__
	Color_Scheme.__table__
	Activity.__table__
	Garment_Activity.__table__
	Base.metadata.create_all(ENGINE)
	print "all tables created."


