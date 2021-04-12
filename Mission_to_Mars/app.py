from flask import Flask
from flask_pymongo import PyMongo

import scrape_mars
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_db_data = mongo.db.mars_db.find_one()
    return render_template("index.html", mars_db_data= mars_db_data)

@app.route('/scrape')
def scrape():
    scrape_mars_data = scrape_mars.scrape1()
    mars_db = mongo.db.mars
    mars_db.update({}, scrape_mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run()