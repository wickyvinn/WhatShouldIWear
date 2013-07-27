from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey, Table
import psycopg2
from random import choice


ENGINE = create_engine("postgresql+psycopg2:///rack")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

session = Session()

Base = declarative_base()
Base.query = Session.query_property()

class Garment_Tag(Base):
	__tablename__ = 'garment_tags'
	id = Column(Integer, primary_key = True)
	garment_id = Column(Integer, ForeignKey('garments.id'))
	tag_id = Column(Integer, ForeignKey('tags.id'))
	tag = relationship("Tag", backref="parent_assocs")

class Garment(Base):
	__tablename__ = "garments"
	id = Column(Integer, primary_key=True)
	keywords = Column(String(20), nullable=False)
	type = Column(String(20), nullable=False)
	color = Column(String(20), nullable=True)

	tag = relationship("Garment_Tag", backref="parent",cascade="all, delete, delete-orphan")

class Tag(Base):
	__tablename__ = "tags"
	id = Column(Integer, primary_key=True)
	style = Column(String(32), nullable=False)

#web input definitions#
def addgarment(garment_tags, keywords, type, color): #grabs styles form the checkbox form
	garment = Garment(keywords=keywords, type=type, color=color)
	session.add(garment)
	session.commit()
	for tag_id in garment_tags: #adds each style to the join table
		new_tag = session.query(Tag).get(tag_id)
		garment_tag=Garment_Tag()
		garment_tag.tag = new_tag
		garment.tag.append(garment_tag)
	session.commit()

				#if you want to delete the relationship garment.tag.remove(specified_tag)

def addtag(tag):
	tag = Tag(style=tag)
	session.add(tag)
	session.commit()

def deletegarment(garment_id):
	garment = session.query(Garment).get(garment_id)
	session.delete(garment)
	session.commit()

# outfit generation. homepage #

def findoutfit(location, tag_id, activity): #tag is the entire tag object from tags table
	print tag_id
	g_tags=session.query(Garment_Tag).filter(Garment_Tag.tag_id==tag_id).all() #Find all garments tagged with this tag. 
	outfits={}
	viable_tops=[]
	viable_bottoms=[]
	viable_shoes=[]
	viable_outerwear=[]
	for g_tag in g_tags:
		garment_id=g_tag.garment_id
		garment=session.query(Garment).get(garment_id)
		if garment.type=="top":
			viable_tops.append(garment)
		elif garment.type=="bottoms":
			viable_bottoms.append(garment)
		elif garment.type=="footwear":
			viable_shoes.append(garment)
		elif garment.type=="outerwear":
			viable_outerwear.append(garment)
	for i in range(1,4):
		num = '%s' %(str(i))
		outfits[num]={}
		outfits[num]["top"]=choice(viable_tops)
		outfits[num]["bottoms"]=choice(viable_bottoms)
		outfits[num]["footwear"]=choice(viable_shoes)
		outfits[num]["outerwear"]=choice(viable_outerwear)
	return outfits #these are all objects from the garments table. 

#selects for the sake of listing#
def select_tags():
	all_tags = session.query(Tag).all()
	return all_tags

def select_garments():
	all_garments = session.query(Garment).order_by(Garment.id.desc()).all()
	return all_garments

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