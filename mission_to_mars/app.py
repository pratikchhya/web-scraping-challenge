from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars
from splinter import Browser

# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_mission= mongo.db.mars_mission.find_one()
    return render_template("index.html", mars = mars_mission)


@app.route("/scrape")
def scrape():
    mars_mission = mongo.db.mars_mission
    mars_data = scrape_mars.scrape()
    mars_mission.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)