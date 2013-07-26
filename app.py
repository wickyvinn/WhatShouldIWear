from flask import Flask, render_template, redirect, request, escape, session, url_for
import model

app = Flask(__name__)

# Keep it secret--Keep it safe.
app.secret_key = 'Vrjwlr4315j/3yX R~fd931!jmN]fjkdl7381/,fff'


@app.route("/")
def index():
    return redirect(url_for('changestuff'))

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


# @app.route("/deletegarment", methods=['POST'])
# def process_deletegarment():
# 	print request.form["garment.id"]
# 	id = request.form["garment.id"]
# 	model.deletegarment(id)
# 	return redirect(url_for('changestuff'))


if __name__ == "__main__":
    app.run(debug=True)
