from flask import Flask, render_template, redirect, request, escape, session, url_for
# import model

app = Flask(__name__)

# Keep it secret--Keep it safe.
app.secret_key = 'Vrjwlr4315j/3yX R~fd931!jmN]fjkdl7381/,fff'


@app.route("/")
def index():
    return "homepage"

## my input pages ##
@app.route("/changestuff", methods=['GET'])
def display_addoutfit():
    return render_template("changestuff.html")


@app.route("/addoutfit", methods=['POST'])
def process_addoutfit():
    return redirect(url_for('index'))

@app.route("/deleteoutfit", methods=['POST'])
def process_deleteoutfit():
    return redirect(url_for('index'))

@app.route("/updateoutfit", methods=['POST'])
def process_updateoutfit():
    return redirect(url_for('index'))


# @app.route("/login", methods=["GET"])
# def display_login():
#     return render_template('login.html')


# @app.route("/login", methods=['POST'])
# def process_login():
#     user = model.valid_login(request.form['email'], request.form['password'])
#     if user:
#         session["user_id"] = user.id
#         return redirect(url_for('index'))
#     else:
#         error = "invalid email/password"
#         return render_template('login.html', error=error)


# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('user_id', None)
#     return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
