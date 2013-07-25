from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey
import psycopg2

ENGINE = create_engine("postgresql+psycopg2:///rack")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

session = Session()

Base = declarative_base()
Base.query = Session.query_property()

class Garment(Base):
	__tablename__ = "garments"
	id = Column(Integer, primary_key=True)
	keywords = Column(String(20), nullable=False)
	type = Column(String(20), nullable=False)
	color = Column(String(20), nullable=True)

	# tag = relationship("Association")

class Tag(Base):
	__tablename__ = "tags"
	id = Column(Integer, primary_key=True)
	style = Column(String(32), nullable=False)

class Garment_Tag(Base):
	__tablename__ = "garment_tags"
	id = Column(Integer, primary_key=True)
	garment_id = Column(Integer, ForeignKey('garments.id'), nullable=False)
	tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False)

	# tag = relationship("Child")
	garment = relationship("Garment", backref=backref("garment_tags", order_by=id))
	tag = relationship("Tag", backref=backref("garment_tags", order_by=id))

#selects for the sake of listing#
def select_tags():
	all_tags = session.query(Tag).all()
	return all_tags

def select_garments():
	all_garments = session.query(Garment).order_by(Garment.id.desc()).all()
	return all_garments

#web input definitions#
def addgarment(garment_tags, keywords, type, color):
	garment = Garment(keywords=keywords, type=type, color=color)
	session.add(garment)
	session.commit()
	for style in garment_tags:
		tagger = Garment_Tag(garment_id=garment.id,tag_id=style)
		session.add(tagger)
		session.commit()

def addtag(tag):
	tag = Tag(style=tag)
	session.add(tag)
	session.commit()

def deletegarment(id):
	garment = session.query(Garment).get(id)
	session.delete(garment)
	session.commit()

# class Outfit(Base):
# 	__tablename__ = "outfits"
# 	id = Column(Integer, primary_key=True)
# 	top = Column(String(64), nullable=False)
# 	bottoms = Column(String(64), nullable=True)
# 	footwear = Column(Integer, nullable=False)
# 	outerwear = Column(String(64), nullable=True)
# 	facewear = Column(String(30), nullable=True)
# 	earrings = Column(String(64), nullable=True)
# 	neckwear = Column(String(64), nullable=True)


#Notes: maybe I can have a garments table: color, type of shirt (key word search-wise, like chiffon blouse or kimono), bottoms 
#needed or no
#then, outfits will be derivatives of those, based on markov chains. 
#then, depending on the tags attached to each garment, we'll just create an assload of combinations with tags attached
#then, when they call the parameters, just pull the outfit that falls under that concept. 

#Notes: it'll only ping an outfit request when someone runs the request. 
#you have garments, with tags attached.
#it'll ping a markov chain from a view containing clothing with those tags. 
#then it'll save the outfit in the outfit table for voting powers. these will be options following the primary option 
#(newly found markov chain)


### table makin ###

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


session.close()








########### NOTES PSYCOPG W.O SQLALCHEMY ###########
# conn = psycopg2.connect(database='rack')
# cur = conn.cursor()

# cur.execute("CREATE TABLE outfits (id serial PRIMARY KEY, top varchar(30), bottoms varchar(30), footwear varchar(30));")
# session.execute("INSERT INTO outfits (top, footwear) VALUES (%s, %s)",("chambray sundress","leather sandals"))
# session.execute("SELECT * FROM outfits;")
# r = session.fetchone()
# print r


