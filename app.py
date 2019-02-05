from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask import render_template


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
        output.append({'vin': v['vin']})

        #output.append({'vehicleSpecification.manufacturer': v['vehicleSpecification.manufacturer']})
#    return jsonify({'result': output})
    return render_template('vehicles.html', vehicles=output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    vehicle = mongo.db.vehicles
    vehicle.getOne({})
    return 'Got Vehicle'

if __name__ == "__main__":
    app.run()

