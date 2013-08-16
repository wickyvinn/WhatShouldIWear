from flask import Flask, render_template, redirect, request, escape, session, url_for
import model
import json

#https://developers.google.com/image-search/v1/devguide#
app = Flask(__name__)
app.secret_key = 'Vrjwlr4315j/3yX R~fd931!jmN]fjkdl7381/,fff'

@app.route("/")
def index():
	all_tags = model.session.query(model.Tag).all()
	return render_template("home.html",all_tags=all_tags)

## my input pages ##
@app.route("/changestuff", methods=['GET'])
def changestuff():
	all_tags = model.session.query(model.Tag).all()
	all_garments = model.session.query(model.Garment).order_by(model.Garment.id.desc()).all()
	return render_template("changestuff.html",all_tags=all_tags, all_garments=all_garments)

@app.route("/addgarment", methods=['POST'])
def process_addgarment():
	keywords=request.form["keywords"]
	type=request.form["type"]
	garment_tags=request.form.getlist("garment_tags")
	model.addgarment(garment_tags=garment_tags, keywords=keywords, type=type)
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

## homepage stuff ##

@app.route("/findoutfit", methods=['POST'])
def findoutfit():
	location=request.form["location"] #activate these later. right now just a string
	tag_id=request.form["tag_id"] #only tag_id
	activity=request.form["activity"] #activate these later. right now just a string 
	outfits=model.findoutfits(location=location, tag_id=tag_id, activity=activity) #return are all garment objects
	json_outfits=model.jsonify_outfits(outfits)
	js_outfit_data = json.dumps(json_outfits, indent=3)
	return render_template("carousel.html",js_outfit_data=js_outfit_data)

@app.route("/garments")
def findproducts():
	garment_id = request.args.get("id")
	products = model.session.query(model.Garment_Search).filter(model.Garment_Search.garment_id == garment_id).all()
	return render_template("garments.html",products=products)

@app.route('/product')
def ajax_product():
	garment_id = request.args.get("id")
	products = model.session.query(model.Garment_Search).filter(model.Garment_Search.garment_id == garment_id).limit(6).all()
	similar_results_json = []
	for product in products:
		similar_results_json.append(model.jsonify_search(product.search))
	return json.dumps(similar_results_json, indent=3)

if __name__ == "__main__":
    app.run(debug=True)