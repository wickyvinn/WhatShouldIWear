from flask import Flask, render_template, redirect, request, escape, session, url_for
import model
import json

#https://developers.google.com/image-search/v1/devguide#
app = Flask(__name__)
app.secret_key = 'Vrjwlr4315j/3yX R~fd931!jmN]fjkdl7381/,fff'

@app.route("/")
def index():
	all_tags = model.select_tags()
	return render_template("home.html",all_tags=all_tags)

## my input pages ##
@app.route("/changestuff", methods=['GET'])
def changestuff():
	all_tags = model.select_tags()
	all_garments = model.select_garments()
	return render_template("changestuff.html",all_tags=all_tags, all_garments=all_garments)

@app.route("/addgarment", methods=['POST'])
def process_addgarment():
	color=request.form["color"]
	keywords=request.form["keywords"]
	type=request.form["type"]
	garment_tags=request.form.getlist("garment_tags")
	model.addgarment(garment_tags=garment_tags, keywords=keywords, type=type, color=color)
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
	outfits=model.searchproducts(outfits)
	outfits=model.jsonify_outfits(outfits)
	js_data = json.dumps(outfits, indent=3)
	return render_template("outfits.html",js_data=js_data)


if __name__ == "__main__":
    app.run(debug=True)