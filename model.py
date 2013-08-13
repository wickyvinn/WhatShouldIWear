from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey, Table, or_
import psycopg2
from random import choice
from database import Garment, Tag, Garment_Tag, Search, Garment_Search, Color_Scheme

ENGINE = create_engine("postgresql+psycopg2:///rack2")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
session = Session()
Base = declarative_base()
Base.query = Session.query_property()

#web input definitions#
def addgarment(garment_tags, keywords, type): #grabs styles form the checkbox form
	garment = Garment(keywords=keywords, type=type)
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
	viable_outerwear=[]
	for g_tag in g_tags:
		garment_id=g_tag.garment_id
		garment=session.query(Garment).get(garment_id)
		if garment.type=="top": viable_tops.append(garment)
		elif garment.type=="dress": viable_dresses.append(garment)	
		elif garment.type=="bottoms": viable_bottoms.append(garment)
		elif garment.type=="footwear": viable_shoes.append(garment)
		elif garment.type=="outerwear": viable_outerwear.append(garment)
	#now you've made the closet available given the params. so you can now choose from it. 
	outfits = []
	for i in range(4):
		outfit = []
		# try:
		# 	outfit.append(choice(viable_dresses))
		# except:
		outfit.append(choice(viable_tops))
		outfit.append(choice(viable_bottoms))
		outfit.append(choice(viable_shoes))
		outfit.append(choice(viable_outerwear))
		outfits.append(outfit)
	return outfits #a list of outfits. each outfit is a list of garment objects. 			

def colorify(outfit, color_scheme):
	for garment in outfit:
		color_search = session.query(Garment_Search).join(Search).filter(Search.color.in_([color_scheme.color1, 
										color_scheme.color2, 
										color_scheme.color3, 
										color_scheme.color4, 
										color_scheme.color5, 
										color_scheme.color6])).filter(Garment_Search.garment_id == garment.id).first()
		garment.colored_search = color_search
	return outfit

def jsonify_outfits(outfits):
	print "jsonifying the outfits"
	outfits_json = []
	for outfit in outfits:

		outfit_json = []
		for garment in outfit:
			garment_json = {"id":garment.id, "keywords":garment.keywords, "type":garment.type}
			outfit_json.append(garment_json)

			garment_json["search"]=[]
			for search in garment.search:
				search_json = jsonify_search(search.search)
				garment_json["search"].append(search_json)

		outfits_json.append(outfit_json)	
	return outfits_json

def jsonify_search(search):
	return {"id":search.id, 
			"url":search.url,
			"title":search.title,
			"companyname":search.companyname,
			"img":search.img,
			"price":search.price,
			"thing_id":search.thing_id,
			"description":search.description,
			"color":search.color,
			"primary":search.primary}

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