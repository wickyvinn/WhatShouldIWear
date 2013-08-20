from flask import Flask, render_template, redirect, request, escape, session, url_for
import model
import json

#https://developers.google.com/image-search/v1/devguide#
app = Flask(__name__)
app.secret_key = 'Vrjwlr4315j/3yX R~fd931!jmN]fjkdl7381/,fff'

@app.route("/")
def index():	
	all_tags = model.session.query(model.Tag).all()
	all_activities = model.session.query(model.Activity).all()
	return render_template("home.html",all_tags=all_tags, all_activities=all_activities)

## my input pages ##
@app.route("/changestuff", methods=['GET'])
def changestuff():
	all_tags = model.session.query(model.Tag).all()
	all_activities = model.session.query(model.Activity).all()
	all_garments = model.session.query(model.Garment).order_by(model.Garment.id.desc()).all()
	return render_template("changestuff.html",all_tags=all_tags, all_garments=all_garments, all_activities = all_activities)

@app.route("/addgarment", methods=['POST'])
def process_addgarment():
	keywords=request.form["keywords"]
	type=request.form["type"]
	garment_tags=request.form.getlist("garment_tags")
	garment_activities=request.form.getlist("garment_activities")
	model.addgarment(garment_tags=garment_tags, garment_activities = garment_activities, keywords=keywords, type=type)
	return redirect(url_for('changestuff'))

@app.route("/updategarment", methods=['POST'])
def process_updategarment():
	garment_id=request.form["garment_id"] #passes the entire garment object
	garment_tags=request.form.getlist("garment_tags")
	garment_activities=request.form.getlist("garment_activities")
	model.updategarment(garment_id = garment_id, garment_tags=garment_tags, garment_activities = garment_activities)
	return redirect(url_for('changestuff'))

@app.route("/addtag", methods=['POST'])
def process_addtag():
	tag=request.form["tag"]
	model.addtag(tag=tag)
	return redirect(url_for('changestuff'))

@app.route("/deletegarment", methods=['POST'])
def process_deletegarment():
	garment_id=request.form["garment_id"] #passes the entire garment object
	model.deletegarment(garment_id)
	return redirect(url_for('changestuff'))

@app.route("/makeprimary", methods=['POST'])
def makeprimary():
	search_id=request.form["search_id"]
	model.makeprimary(search_id)
	return redirect(url_for('changestuff'))

## homepage stuff ##

@app.route("/findoutfit", methods=['POST'])
def findoutfit():
	location=request.form["location"] # zipcode, a string. pywapi accepts a string. 
	tag_id=request.form["tag_id"] #only tag_id
	activity_id=request.form["activity_id"]
	json_outfits=model.findoutfits(location=location, tag_id=tag_id, activity_id=activity_id) #return are all garment objects
	js_outfit_data = json.dumps(json_outfits, indent=3)
	return render_template("carousel.html",js_outfit_data=js_outfit_data)
	# return render_template(tag_id, activity_id)

@app.route("/garments")
def findproducts():
	garment_id = request.args.get("id")
	products = model.session.query(model.Garment_Search).filter(model.Garment_Search.garment_id == garment_id).all()
	return render_template("garments.html",products=products)

@app.route('/scrap')
def scrap():
	return render_template('scrap.html')

@app.route('/product')
def ajax_product():
	garment_id = request.args.get("id")
	products = model.session.query(model.Garment_Search).filter(model.Garment_Search.garment_id == garment_id).all()
	similar_results_json = []
	for product in products:
		similar_results_json.append(model.jsonify_search(product.search))
	return json.dumps(similar_results_json, indent=3)

if __name__ == "__main__":
    app.run(debug=True)