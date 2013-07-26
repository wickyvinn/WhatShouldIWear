from model import Garment, Tag, make_garments_table, make_tags_table, make_garment_tags_table
from sqlalchemy.ext.declarative import declarative_base
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


ENGINE = create_engine("postgresql+psycopg2:///rack_ass")
Session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))

session = Session()
Base = declarative_base()
Base.query = Session.query_property()

def load_garments(session):
	make_garments_table()
	with open('seed_files/garments', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Garment(id=row[0],
						keywords=row[1],
						type=row[2],
						color=row[3])
			session.add(u)
	session.commit()
	print "loaded garments"

def load_tags(session):
	make_tags_table()
	with open('seed_files/tags', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Tag(id=row[0],
					style=row[1])
			session.add(u)
	session.commit()
	print "loaded tags"

def load_garment_tags(session):
	#make_garment_tags_table()
	with open('seed_files/garment_tags', 'rb') as data_file:
		datareader = csv.reader(data_file, delimiter='|')
		for row in datareader:
			u = Garment_Tag(garment_id=row[0],
					tag_id=row[1])
			session.add(u)
	session.commit()
	print "loaded garment_tags"	

# import psycopg2

# conn = psycopg2.connect(database='rack')
# cur = conn.cursor()
# 	cur.execute("INSERT INTO tags (style) VALUES (%s)",(style,))
# 	cur.execute("SELECT * FROM outfits;")

# conn.commit()