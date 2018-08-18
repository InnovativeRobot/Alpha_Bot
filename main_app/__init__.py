from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('default.html') 

@app.route("/about", methods=["GET"])
def about():
    return  render_template('about.html') 



@app.route('/showMap', methods=["GET"])
def showMap():
    return render_template('showMap.html') 