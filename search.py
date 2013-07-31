#!/usr/bin/python
import json
import urllib2

def garment_search(keywords_raw):
	key = 'key'
	cx = 'cx'
	keywords = keywords_raw.replace(' ','%20')
	url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" \
			%(str(key), str(cx), str(keywords))
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req)
	json_dict = json.load(f)
	
	# list_of_search_results = []
	items_dict = json_dict.get("items") #each cse call returns a list of "items", which are each grouping of urls found. 

	for i in range(len(items_dict)):
		search_result = {} #each item will have a dictionary called search_result
		search_result["title"] = items_dict[i].get("title")
		search_result["displayLink"] = items_dict[i].get("displayLink")
		
		try: 
			metatags = items_dict[i].get("pagemap").get("metatags") 

			#metatags is where the product url and image usually reside. eventually only garments
			#containing these data will be used to generate outfits. UNLESS we can search_result images from the site. maybe. 
			#it's annoying because metatags is a list of dictionaries, 
			#but let's just assume the first one is the only one we care about.

			search_result["url"] = megatags[0].get("og:url")
			search_result["image"] = megatags[0].get("og:image")			
		except:
			print "og url and og image not available."

		search_result["link"] = items_dict[i].get("link")
		# list_of_search_results.append(search_result)
	return search_result



#sample #
#https://www.googleapis.com/customsearch/v1?key=key&cx=cx&q=white%20collared%20shirt

#cse set up
#https://www.google.com/cse/setup/basic?cx=016612632526408655730:z0jhqf-1kro
#https://code.google.com/apis/console/?pli=1#project:961779558939:access


#json tutorial
#http://stackoverflow.com/questions/1640715/get-json-data-via-url-and-use-in-python-simplejson