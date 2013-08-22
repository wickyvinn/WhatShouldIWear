from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine,\
						ForeignKey, Table, or_
import psycopg2
from random import choice
from database import Garment, Tag, Garment_Tag, Search, Garment_Search, Color_Scheme, Activity, Garment_Activity
from pywapi import get_weather_from_yahoo as get_weather

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

def makeprimary(search_id): #curate primary images.
	search_id = int(float(search_id))
	garment_search=session.query(Garment_Search).filter(Garment_Search.search_id == search_id).one()
	garment_search.search.primary=1 #set new primary

	#get rid of old primaries. 
	garment=session.query(Garment).get(garment_search.garment_id) #get all_related_products
	session.commit()
	session.refresh(garment_search)
	for each_garment_search in garment.search:
		if each_garment_search.search_id == search_id:
			pass
		else:
			each_garment_search.search.primary=0
			print each_garment_search.search_id,"NOT primary"
			session.commit()
			session.refresh(each_garment_search)

	session.commit()
	print "made",search_id,"primary."


# outfit generation. homepage #
def findoutfits(tag_id, activity_id, location = None):

	#query looks for all clothes that fall under the tag and activity params. 

	query = """SELECT gg.garment_id, gg.type FROM 
	(SELECT garment_id, type FROM garments JOIN garment_tags as gt 
		on garments.id = gt.garment_id 
		WHERE tag_id = %s) as gg 
	JOIN garment_activities as ga 
		ON ga.garment_id = gg.garment_id 
		WHERE ga.activity_id = %s;""" %(tag_id, activity_id)
	cur.execute(query, (tag_id, activity_id))
	all_garments = cur.fetchall()

	weather_report = get_weather(location)
	high_temp = int(float(weather_report['forecasts'][-1]['high']))
	
	outfits={} 

	#go through tags/activities and find outfit concepts
	viable_tops=[]
	viable_dresses=[]
	viable_bottoms=[]
	viable_shoes=[]
	viable_outerwear=[]
	viable_accessories=[]
	viable_bags=[]

	for garment in all_garments: 

	#you grabbed two columns from the query above. garment id and type. we check row[1] for type,
								#and then append the id to our viable tops closet. 
	
		if garment[1]=="top": viable_tops.append(garment[0]) 
		elif garment[1]=="dress": viable_dresses.append(garment[0])	
		elif garment[1]=="bottoms": viable_bottoms.append(garment[0])
		elif garment[1]=="footwear": viable_shoes.append(garment[0])
		elif garment[1]=="outerwear": viable_outerwear.append(garment[0])
		elif garment[1]=="accessory": viable_accessories.append(garment[0])
		elif garment[1]=="bag": viable_bags.append(garment[0])

	#now you've made the closet available given the params. so now choose from it. 

	outfits = []

	tag = session.query(Tag).get(tag_id)
	activity = session.query(Activity).get(activity_id)

	for i in range(4):
		outfit = []

		#dress it up. if romantic, bohemian or chic, or going to the club we'll stick a a dress or two in there. 
		
		if high_temp>22:	#if it's over 70ish degrees
			if tag.style != "tomboy" and i != 2 and not (activity.activity == "errands"): #as long as we're not tomboys, put a dress at first outfit
				print "hot dress time"
				#-----
				index=range(len(viable_dresses))
				i = choice(index)
				outfit.append(session.query(Garment).get(viable_dresses[i]))
				index.pop(i)
				#-----
				# chosen_dress = choice(viable_dresses)
				# outfit.append(session.query(Garment).get(chosen_dress))
				#-----
				outfit.append(session.query(Garment).get(choice(viable_accessories)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_bags)))
			else: #tomboys don't feel like wearing dresses right now. and you don't when you're running errands too. 
				print "tomboy wears bag/accessories instead"
				outfit.append(session.query(Garment).get(choice(viable_tops)))
				
				if i != 1: #we give the tomboy a bag most of the time. 
					outfit.append(session.query(Garment).get(choice(viable_bags)))	
				else:
					outfit.append(session.query(Garment).get(choice(viable_accessories)))
				
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_bottoms)))
		else:
			if (tag.style == "romantic" and i!=2) or ((tag.style == "bohemian" or tag.style =="chic") and i==2) or (activity.activity == "club" and i != 3) or (activity_id == "date" and i==2): #if tag is romantic
				print "cold dress time!"			
				index=range(len(viable_dresses))
				i = choice(index)
				outfit.append(session.query(Garment).get(viable_dresses[i]))
				index.pop(i)

				# outfit.append(session.query(Garment).get(choice(viable_dresses)))
				outfit.append(session.query(Garment).get(choice(viable_bags)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_outerwear)))
			else:
				print "cold pants time"
				outfit.append(session.query(Garment).get(choice(viable_tops)))
				outfit.append(session.query(Garment).get(choice(viable_bottoms)))
				outfit.append(session.query(Garment).get(choice(viable_shoes)))
				outfit.append(session.query(Garment).get(choice(viable_outerwear)))

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
	outfits_json = []

	for outfit in outfits:

		outfit_json = []
		for garment in outfit:
			garment_json = {"id":garment.id, "keywords":garment.keywords, "type":garment.type}
			garment_json["search"]=[]
			for i in range(len(garment.search)):
				try:
					search_json = jsonify_search(garment.search[i].search)
					garment_json["search"].append(search_json)
				except: 
					pass
			if garment_json["search"]==[]:
				garment_json["search"]=None
			outfit_json.append(garment_json)
		outfits_json.append(outfit_json)	
	return outfits_json

def jsonify_search(search):
	return {"id":search.id, "url":search.url,"title":search.title,"companyname":search.companyname,"img":search.img,"price":search.price,"thing_id":search.thing_id,"color":search.color, "primary":search.primary}

session.close()