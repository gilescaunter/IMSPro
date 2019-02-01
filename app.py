from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = "bims-uat"
app.config['MONGO_URI'] = "mongodb://localhost:27017/bims-uat"

mongo = PyMongo(app)

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicle = mongo.db.vehicles
    output = []
    for v in vehicle.find():
        output.append({'regNo': v['regNo']})
    return jsonify({'result': output})

@app.route('/')
def index():
    return "hello flask"

@app.route('/view')
def view():
    vehicle = mongo.db.vehicles
    vehicle.getOne({})
    return 'Got Vehicle'

if __name__ == "__main__":
    app.run()

