#!/usr/bin/python
import json
from bs4 import BeautifulSoup
import requests
import time
from database import Search, Garment, Garment_Search, ENGINE, session

def add_polyvore(garment_object,color):
	print "acquiring polyvore search results"
	formatted_keywords = garment_object.keywords.replace(' ','+')
	keywords_color = formatted_keywords+'+%s' %str(color)
	query = "http://www.polyvore.com/cgi/shop?price.currency=USD&price.from=0&price.to=200&query=%s&_out=json" %(str(keywords_color))
	r = requests.get(query, allow_redirects=False)	
	print query
	try:
		json_dict = r.json()
		items = json_dict['result']['items'] #just the way their page is set up. 


		num_successful_searches = 0

		for i in range(len(items)): #go through the whole search result dictionary
			
			count = 0 #make sure that title matches our keyword search ((enough))
			count2 = 0

			for keyword in garment_object.keywords.split():
				if keyword.lower() in items[i]['title'].lower():
					print keyword.lower(),'in title'
					count += 1

			for keyword in garment_object.keywords.split():
				if keyword.lower() in items[i]['description'][0:1000].lower():
					print keyword.lower(),'in description'
					count2 += 1

			length = len(garment_object.keywords.split())

			if ((count/length) >= .60) or ((count2/length) >= .80): 
											# at least two-thirds of title_words same as keywords
											# you may want to add color in as a mandatory requirement. 
				url = items[i]["url"]
				title = items[i]['title']
				companyname = items[i]['displayurl']
				img = 'http://ak2.polyvoreimg.com/cgi/img-thing/size/l/tid/%s.jpg' %(str(items[i]['thing_id']))
				price = items[i]['display_price'] #price is an integer of cents.
				thing_id = items[i]['thing_id']
				description = items[i]['description'][0:400]

				#check if the search item exists. 
				existing_search_object = session.query(Search).filter_by(thing_id=thing_id).first()

				if existing_search_object: #update
					existing_search_object.url = url
					existing_search_object.title = title
					existing_search_object.companyname = companyname
					existing_search_object.price = price # obviously thing id is the same, and correspondingly, so is img. 
					num_successful_searches += 1

					existing_garment_search_object = session.query(Garment_Search).filter(Garment_Search.search_id == existing_search_object.id).one()

					if existing_garment_search_object:
						pass
					else:
						garment_search = Garment_Search(garment_id = garment_object.id, search_id = existing_search_object.id)
						session.add(garment_search)
						session.commit()
						print "existing is childless, added garment_search adopted child."
					print ".........EXISTING.","thing_id:",thing_id,"........."

				else: 
					search = Search(url = url,
									title = title,
									companyname = companyname,
									img = img,
									price = price, #price is a string due to $ and pounds symbols. 
									thing_id = thing_id,
									description = description,
									primary=0,
									color = color)
					session.add(search)
					print "search added"
					session.commit()

					session.refresh(search) # gotta commit and refresh in order to grab newly added search_id
					garment_search = Garment_Search(garment_id = garment_object.id, search_id = search.id)
					session.add(garment_search)
					session.commit()
					print "ADDED A SEARCH...\n"
					num_successful_searches += 1

			if num_successful_searches == 2: # we're going to try to pull five results every time. might be less if we dont get good ones. 
											 # keep in mind that each garment can have more than five results 
											 # in the database if results are new every time you run. 
											 # later, be sure to only request so many in our templates. 
				break #end the loop. 
		
	except:
		print "nothing added for this color"

	session.commit() #add them and update existing records. 
	print "committed results."


if __name__ == '__main__': #so if we import from search, it doesn't run these but only when we run search.py (aka when the "main" module is search.py)
	all_garments = session.query(Garment).all()
	colors = ['','black','blue','red','green','gray','white','yellow']
	for garment in all_garments[5:]:
		for color in colors:
			print color, garment.keywords,":"
			add_polyvore(garment, color)
	print "done for today. zzz..."
	time.sleep(86400)