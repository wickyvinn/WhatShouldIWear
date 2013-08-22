from database import Garment, Tag, Garment_Tag, Search, Garment_Search, Color_Scheme, Activity, Garment_Activity, make_garments_table, make_tags_table, make_garment_tags_table
from sqlalchemy.ext.declarative import declarative_base
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


ENGINE = create_engine("postgresql+psycopg2:///rack")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

session = Session()
Base = declarative_base()
Base.query = Session.query_property()

def load_garments(session):
	with open('seed_files/garments', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Garment(keywords=row[0],
						type=row[1])
			session.add(u)
	session.commit()
	print "loaded garments"

def load_tags(session):
	with open('seed_files/tags', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Tag(style=row[0])
			session.add(u)
	session.commit()
	print "loaded tags"

def load_garment_tags(session):
	with open('seed_files/garment_tags', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Garment_Tag(garment_id=row[0],
					tag_id=row[1])
			session.add(u)
	session.commit()
	print "loaded garment_tags"	

def load_activities(session):
	with open('seed_files/activities', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Activity(activity=row[0])
			session.add(u)
	session.commit()
	print "loaded activities"	 

def load_color_schemes(session):
	with open('seed_files/color_schemes', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			color1 = None
			color2 = None
			color3 = None
			color4 = None
			color5 = None
			color6 = None
			try:
				color1=row[0]
				color2=row[1]
				color3=row[2]
				color4=row[3]
				color5=row[4]
				color6=row[5]
			except:
				pass
			u = Color_Scheme(color1=color1,
								color2=color2,
								color3=color3,
								color4=color4,
								color5=color5,
								color6=color6)
			session.add(u)
	session.commit()
	print "loaded color_schemes"