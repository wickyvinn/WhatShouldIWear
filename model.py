from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey, Table
import psycopg2
from random import choice
#import search

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
	search = relationship("Garment_Search", backref="parent",cascade="all, delete, delete-orphan")

	def __init__(self):
		self.id = id
		self.keywords = keywords
		self.type = type
		self.color = color
	
	def jsonify(self):
		return {"id":self.id, "keywords":self.keywords, "type":self.type, "color":self.color}

class Search(Base):
	__tablename__ = 'searches'
	id = Column(Integer, primary_key = True)
	url = Column(String(300), nullable = True)
	title = Column(String(200), nullable = True)
	companyname = Column(String(48), nullable = True)
	img = Column(String(300), nullable = True)
	price = Column(String(20), nullable = True)
	thing_id = Column(Integer, nullable = True)

class Garment_Search(Base):
	__tablename__ = 'garment_searches'
	id = Column(Integer, primary_key = True)
	garment_id = Column(Integer, ForeignKey('garments.id'))
	search_id = Column(Integer, ForeignKey('searches.id'))
	search = relationship("Search", backref="parent_assocs")

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
def findoutfits(tag_id, location = None, activity = None):
	print "finding outfits"
	g_tags=session.query(Garment_Tag).filter(Garment_Tag.tag_id==tag_id).all() #Find all garments tagged with this tag. 
	outfits={} #go through tags and find outfit concepts. markov shit will probably go here too. 
	viable_tops=[]
	viable_dresses=[]
	viable_bottoms=[]
	viable_shoes=[]
	#viable_outerwear=[]
	for g_tag in g_tags:
		garment_id=g_tag.garment_id
		garment=session.query(Garment).get(garment_id)
		if garment.type=="top": viable_tops.append(garment)
		elif garment.type=="dress": viable_dresses.append(garment)	
		elif garment.type=="bottoms": viable_bottoms.append(garment)
		elif garment.type=="footwear": viable_shoes.append(garment)
		# elif garment.type=="outerwear": viable_outerwear.append(garment)
	#now you've made the closet available given the params. so you can now choose from it. 
	outfits = []
	for i in range(3):
		outfit = []
		outfit.append(choice(viable_tops))
		outfit.append(choice(viable_bottoms))
		# outfit.append(choice(viable_outerwear))
		outfit.append(choice(viable_shoes))
		outfits.append(outfit)
	return outfits #a list of outfits. each outfit is a list of garment objects. 			

def jsonify_outfits(outfits):
	print "jsonifying the outfits"
	outfits_json = []
	for outfit in outfits:
		outfit_json = []
		for garment in outfit:
			garment_json = {"id":garment.id, "keywords":garment.keywords, "type":garment.type, "color":garment.color,
			'search_results':garment.search_results.json}
			outfit_json.append(garment_json)
		outfits_json.append(outfit_json)	
	return outfits_json

### table makin ###

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