from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey, Table, or_
import psycopg2
from random import choice
from database import Garment, Tag, Garment_Tag, Search, Garment_Search, Color_Scheme, Activity, Garment_Activity

ENGINE = create_engine("postgresql+psycopg2:///rack")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
session = Session()
Base = declarative_base()
Base.query = Session.query_property()

conn = psycopg2.connect(database='rack')
cur = conn.cursor()


#web input definitions#
def addgarment(garment_tags, garment_activities, keywords, type): #grabs styles form the checkbox form
	garment = Garment(keywords=keywords, type=type)
	session.add(garment)
	session.commit()
	for tag_id in garment_tags: #adds each style to the join table
		new_tag = session.query(Tag).get(tag_id)
		garment_tag=Garment_Tag()
		garment_tag.tag = new_tag
		garment.tag.append(garment_tag)
	for activity_id in garment_activities:
		new_activity = session.query(Activity).get(activity_id)
		garment_activity=Garment_Activity()
		garment_activity.activity = new_activity
		garment.activity.append(garment_activity)
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

def updategarment(garment_id, garment_tags, garment_activities):
	garment = session.query(Garment).get(garment_id)		
	for tag_id in garment_tags: #adds each style to the join table
		new_tag = session.query(Tag).get(tag_id)
		garment_tag=Garment_Tag()
		garment_tag.tag = new_tag
		garment.tag.append(garment_tag)
	for activity_id in garment_activities:
		new_activity = session.query(Activity).get(activity_id)
		garment_activity=Garment_Activity()
		garment_activity.activity = new_activity
		garment.activity.append(garment_activity)
	session.commit()


# outfit generation. homepage #
def findoutfits(tag_id, activity_id, location = None):

	query = """SELECT gg.garment_id, gg.type FROM 
	(SELECT garment_id, type FROM garments JOIN garment_tags as gt 
		on garments.id = gt.garment_id 
		WHERE tag_id = %s) as gg 
	JOIN garment_activities as ga 
		ON ga.garment_id = gg.garment_id 
		WHERE ga.activity_id = %s;"""
	cur.execute(query, (tag_id, activity_id))
	all_garments = cur.fetchall()


	# g_tags=session.query(Garment_Tag).filter(Garment_Tag.tag_id==tag_id).all() #Find all garments tagged with this tag. 
	outfits={} 

	#go through tags and find outfit concepts. markov shit will probably go here too. 
	viable_tops=[]
	viable_dresses=[]
	viable_bottoms=[]
	viable_shoes=[]
	viable_outerwear=[]
	viable_accessories=[]
	viable_bags=[]

	# for g_tag in g_tags:
	# 	garment_id=g_tag.garment_id
	# 	garment=session.query(Garment).get(garment_id)
	
	for garment in all_garments:
		if garment[1]=="top": viable_tops.append(garment[0])
		elif garment[1]=="dress": viable_dresses.append(garment[0])	
		elif garment[1]=="bottoms": viable_bottoms.append(garment[0])
		elif garment[1]=="footwear": viable_shoes.append(garment[0])
		elif garment[1]=="outerwear": viable_outerwear.append(garment[0])
		elif garment[1]=="accessory": viable_accessories.append(garment[0])
		elif garment[1]=="bag": viable_bags.append(garment[0])

	#now you've made the closet available given the params. so you can now choose from it. 
	outfits = []
	for i in range(4):
		outfit = []

		#dress it up. if romantic, bohemian or chic, or going to the club we'll stick a a dress or two in there. 
		
		if location=="hot":	#if it's over 70 degrees
			if tag_id != "6" and i != 2: #as long as we're not tomboys, put a dress at first outfit
				print "hot dress time"
				outfit.append(session.query(Garment).get(choice(viable_dresses)))
				outfit.append(session.query(Garment).get(choice(viable_accessories)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_bags)))
			else: #tomboys don't feel like wearing dresses right now. 
				print "tomboy wears bag/accessories instead"
				outfit.append(session.query(Garment).get(choice(viable_tops)))
				if i != 1: #we give the tomboy a bag most of the time. 
					outfit.append(session.query(Garment).get(choice(viable_bags)))	
				else:
					outfit.append(session.query(Garment).get(choice(viable_accessories)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_bottoms)))
		else:
			if (tag_id == "2" and i!=2) or ((tag_id == "4" or tag_id =="1") and i==2) or (activity_id == "6" and i != 3) or (activity_id == "3" and i==2): #if tag is romantic
				print "cold dress time!"			
				outfit.append(session.query(Garment).get(choice(viable_dresses)))
				outfit.append(session.query(Garment).get(choice(viable_accessories)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_bags)))
			else:
				print "cold pants time"
				outfit.append(session.query(Garment).get(choice(viable_tops)))
				outfit.append(session.query(Garment).get(choice(viable_bottoms)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_outerwear)))
	# 	# color_scheme = session.query(Color_Scheme).get(38)
	# 	# outfit_colorified = colorify(outfit, color_scheme)
		outfits.append(outfit)
	outfits_json = jsonify_outfits(outfits)
	return outfits_json #a list of outfits. each outfit is a list of garment objects (well, jsonified.)		

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
			garment_json["search"]=[]
			for i in range(5):
				try:
					search_json = jsonify_search(garment.search[i].search)
					garment_json["search"].append(search_json)
				except: 
					pass
			if garment_json["search"]==[]:
				garment_json["search"]=None
				# try: garment_json["colored_search"]=jsonify_search(garment.colored_search.search)
				# except: garment_json["colored_search"]=None

			outfit_json.append(garment_json)
		outfits_json.append(outfit_json)	
	return outfits_json

def jsonify_search(search):
	return {"id":search.id, "url":search.url,"title":search.title,"companyname":search.companyname,"img":search.img,"price":search.price,"thing_id":search.thing_id,"color":search.color, "primary":search.primary}

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