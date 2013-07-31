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
	return json_dict



#sample #
#https://www.googleapis.com/customsearch/v1?key=key&cx=cx&q=white%20collared%20shirt

#cse set up
#https://www.google.com/cse/setup/basic?cx=016612632526408655730:z0jhqf-1kro
#https://code.google.com/apis/console/?pli=1#project:961779558939:access


#json tutorial
#http://stackoverflow.com/questions/1640715/get-json-data-via-url-and-use-in-python-simplejson