#!/usr/bin/python
import json
from bs4 import BeautifulSoup
import requests
import time
from model import Search, Garment, Garment_Search, ENGINE, session

def add_polyvore(garment_object):
	print "acquiring polyvore search results"
	formatted_keywords = garment_object.keywords.replace(' ','+')
	r = requests.get("http://www.polyvore.com/cgi/shop?price.currency=USD&price.from=0&price.to=200&query=%s&_out=json"
		%(str(formatted_keywords)), allow_redirects=False)	
	json_dict = r.json()
	items = json_dict['result']['items'] #just the way their page is set up. 

	num_successful_searches = 0

	for i in range(len(items)): #go through the whole search result dictionary
		
		count = 0 #make sure that title matches our keyword search ((enough))

		for keyword in garment_object.keywords.split():
			if keyword.lower() in items[i]['title'].lower():
				count += 1

		if count/(len(garment_object.keywords.split())) > .66: 
										# at least two-thirds of title_words same as keywords
										# you may want to add color in as a mandatory requirement. 
			url = items[i]["url"]
			title = items[i]['title']
			companyname = items[i]['displayurl']
			img = 'http://ak2.polyvoreimg.com/cgi/img-thing/size/l/tid/%s.jpg' %(str(items[i]['thing_id']))
			price = items[i]['display_price'] #price is an integer of cents.
			thing_id = items[i]['thing_id']

			#check if the search item exists. 
			existing_search_object = session.query(Search).filter_by(thing_id=thing_id).first()

			if existing_search_object: #update
				existing_search_object.url = url
				existing_search_object.title = title
				existing_search_object.companyname = companyname
				existing_search_object.price = price # obviously thing id is the same, and correspondingly, so is img. 
				num_successful_searches += 1

			else: 
				search = Search(url = url,
								title = title,
								companyname = companyname,
								img = img,
								price = price, #price is a string due to $ and pounds symbols. 
								thing_id = thing_id)
				session.add(search)
				session.commit()
				session.refresh(search) # gotta commit and refresh in order to grab newly added search_id
				garment_search = Garment_Search(garment_id = garment_object.id, search_id = search.id)
				session.add(garment_search)
				num_successful_searches += 1

		if num_successful_searches == 25: # we're going to try to pull five results every time. might be less if we dont get good ones. 
										 # keep in mind that each garment can have more than five results 
										 # in the database if results are new every time you run. 
										 # later, be sure to only request so many in our templates. 
			break #end the loop. 

	session.commit() #add them and update existing records. 
	print "committed results."


if __name__ == '__main__': #so if we import from search, it doesn't run these but only when we run search.py (aka when the "main" module is search.py)
	all_garments = session.query(Garment).all()

	for garment in all_garments:
		add_polyvore(garment)

	print "done for today. zzz..."
	time.sleep(86400)


# class Product(object):
# 	def __init__(self, title, url, img, companyname, price):
# 		self.title = title
# 		self.url = url
# 		self.img = img
# 		self.companyname = companyname
# 		self.price = price

# class Result(object): #each result is a list of Product objects. Each 
# 	def __init__(self, keywords):
# 		self.keywords = keywords
# 		self.split_keywords = keywords.split()
# 		self.products = [] #populates everytime you run polyvore on it. 
# 		self.json = []#the result object itself has an attribute that is a json rendering of self.products

# 	def polyvore(self): 
# 		self.products = []
# 		frm_keywords = self.keywords.replace(' ',"+")
# 		r = requests.get("http://www.polyvore.com/cgi/shop?price.currency=USD&price.from=0&price.to=200&query=%s&_out=json" %(str(frm_keywords)), allow_redirects=False)
# 		json_dict = r.json()
# 		items = json_dict["result"]["items"]
# 		for i in range(len(items)): 
# 			count=0 #make sure that our title matches two words in our search so we don't get crap results. 
# 			for keyword in self.split_keywords: 
# 				if keyword.lower() in items[i]["title"].lower():
# 					count += 1
# 			if count>1:
# 				self.product = Product(title=items[i]["title"].lower(), 
# 								url = items[i]["url"],
# 								thing_id = items[i]['thing_id'],
# 								img='http://ak2.polyvoreimg.com/cgi/img-thing/size/l/tid/%s.jpg' %(str(thing_id)),
# 								companyname = items[i]["displayurl"],
# 								price = items[i]["display_price"]
# 								)
# 				self.products.append(self.product) #if you want to call any of these: result.polyvore()[0].url, result being what you instantiate the Result on. 
# 			if len(self.products) == 5: #we only really need five results. 
# 				break
# 		return self.products

# 	def jsonify(self):
# 		#once you run polyvore on it, you can make it a json object if necessary.
# 		json = []
# 		for r in self.products:
# 			result = {"title": r.title, "url": r.url, "img": r.img, "companyname": r.companyname, "price": r.price}
# 			self.json.append(result)
# 		return self.json

# def nastygal(keywords_raw):
# 	keywords = keywords_raw.replace(' ','+')
# 	r = requests.get('http://www.nastygal.com/index.cfm?fuseaction=search.results&searchString=%s' %(str(keywords)))
# 	soup = BeautifulSoup(r.content)
# 	list_of_search_results = []
# 	products = soup.find_all('div', class_='product') #we grab all the product tags. 
# 	for i in products:
# 		result = {}
# 		image = i.find('div', class_='image') #look for all image tags WITHIN the product tag
# 		price = i.find('div', class_='price') #look for the price tag WITHIN the product tag
# 		result['title'] = image.a['title'] #found in a tag of the image tag
# 		result['url'] = image.a['href'] #same 
# 		result['company_name'] = "nastygal.com"
# 		result['img'] = image.img["src"] #found in the img tag of the image tag
# 		result['price'] = price.span.string #found in the span tag of the price tag. use "string" when you only want the stuff inside. 
# 		list_of_search_results.append(result)
# 	return list_of_search_results

# def asos(keywords_raw):
# 	keywords_minus = keywords_raw.replace(' ','-')
# 	keywords_plus = keywords_raw.replace(' ','+')
# 	r = requests.get('http://us.asos.com/search/%s?hrd=1&q=%s#parentID=Rf-700&pge=0&pgeSize=36&sort=-1%s' %(str(keywords_minus), str(keywords_plus), str('&state=Rf-700%3D1000')))
# 	soup = BeautifulSoup(r.content)
# 	list_of_search_results = []
# 	itemwrapper = soup.find('div', {'id':'items-wrapper', 'class':'items'})
# 	list_li =  itemwrapper.find_all('li') #all found in a bunch of li tags, fucking annoying. 
# 	list_of_search_results=[]
# 	for item in list_li:
# 		result = {}
# 		image = item.find('div', class_="categoryImageDiv")
# 		price = item.find('div', class_="productprice")	
# 		result['url'] = image.a['href']
# 		result['title'] = image.a['title']
# 		result['img'] = image.img['src']
# 		result['price'] = price.find('span', class_='price').string
# 		list_of_search_results.append(result)
# 	return list_of_search_results