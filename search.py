#!/usr/bin/python
import json
import urllib2
from bs4 import BeautifulSoup
import requests

class Product(object):
	def __init__(self, title, url, img, companyname, price):
		self.title = title
		self.url = url
		self.img = img
		self.companyname = companyname
		self.price = price

class Result(object): #each result is a list of Product objects. Each 
	def __init__(self, keywords):
		self.keywords = keywords
		self.split_keywords = keywords.split()
		self.products = [] #populates everytime you run polyvore on it. 
		self.json = []#the result object itself has an attribute that is a json rendering of self.products

	def polyvore(self): 
		self.products = []
		frm_keywords = self.keywords.replace(' ',"+")
		r = requests.get("http://www.polyvore.com/cgi/shop?price.currency=USD&price.from=0&price.to=200&query=%s&_out=json" %(str(frm_keywords)), allow_redirects=False)
		json_dict = r.json()
		items = json_dict["result"]["items"]
		for i in range(len(items)): 
			count=0 #make sure that our title matches two words in our search so we don't get crap results. 
			for keyword in self.split_keywords: 
				if keyword.lower() in items[i]["title"].lower():
					count += 1
			if count>1:
				self.product = Product(title=items[i]["title"].lower(), 
								url = items[i]["url"],
								thing_id = items[i]['thing_id']
								img='http://ak2.polyvoreimg.com/cgi/img-thing/size/l/tid/%s.jpg' %(str(thing_id)),
								companyname = items[i]["displayurl"],
								price = items[i]["display_price"]
								)
				self.products.append(self.product) #if you want to call any of these: result.polyvore()[0].url, result being what you instantiate the Result on. 
			if len(self.products) == 5: #we only really need five results. 
				break
		return self.products

	def jsonify(self):
		#once you run polyvore on it, you can make it a json object if necessary.
		json = []
		for r in self.products:
			result = {"title": r.title, "url": r.url, "img": r.img, "companyname": r.companyname, "price": r.price}
			self.json.append(result)
		return self.json

def nastygal(keywords_raw):
	keywords = keywords_raw.replace(' ','+')
	r = requests.get('http://www.nastygal.com/index.cfm?fuseaction=search.results&searchString=%s' %(str(keywords)))
	soup = BeautifulSoup(r.content)
	list_of_search_results = []
	products = soup.find_all('div', class_='product') #we grab all the product tags. 
	for i in products:
		result = {}
		image = i.find('div', class_='image') #look for all image tags WITHIN the product tag
		price = i.find('div', class_='price') #look for the price tag WITHIN the product tag
		result['title'] = image.a['title'] #found in a tag of the image tag
		result['url'] = image.a['href'] #same 
		result['company_name'] = "nastygal.com"
		result['img'] = image.img["src"] #found in the img tag of the image tag
		result['price'] = price.span.string #found in the span tag of the price tag. use "string" when you only want the stuff inside. 
		list_of_search_results.append(result)
	return list_of_search_results

def asos(keywords_raw):
	keywords_minus = keywords_raw.replace(' ','-')
	keywords_plus = keywords_raw.replace(' ','+')
	r = requests.get('http://us.asos.com/search/%s?hrd=1&q=%s#parentID=Rf-700&pge=0&pgeSize=36&sort=-1%s' %(str(keywords_minus), str(keywords_plus), str('&state=Rf-700%3D1000')))
	soup = BeautifulSoup(r.content)
	list_of_search_results = []
	itemwrapper = soup.find('div', {'id':'items-wrapper', 'class':'items'})
	list_li =  itemwrapper.find_all('li') #all found in a bunch of li tags, fucking annoying. 
	list_of_search_results=[]
	for item in list_li:
		result = {}
		image = item.find('div', class_="categoryImageDiv")
		price = item.find('div', class_="productprice")	
		result['url'] = image.a['href']
		result['title'] = image.a['title']
		result['img'] = image.img['src']
		result['price'] = price.find('span', class_='price').string
		list_of_search_results.append(result)
	return list_of_search_results