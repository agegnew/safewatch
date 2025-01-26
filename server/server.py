import flask

app = flask.Flask(__name__)

@app.route("/")
def get_home_page():
    return flask.render_template("index.html")



app.run(host="0.0.0.0", port=5000)