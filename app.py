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
    for v in vehicle.find(projection = {'regNo':1, 'vehicleSpecification.manufacturer':1,'status.0.processName':1}):
        line = {}
        line['regNo'] = v.get('regNo','-')
        if 'vehicleSpecification.manufacturer' in v:
            line['manufacturer'] = v['vehicleSpecification']['manufacturer']
        else:
            line['manufacturer'] = '-'
        if 'vehicleSpecification.model' in v:
            line['model'] = v['vehicleSpecification']['model']
        else:
            line['model'] = '-'
        if 'vehicleSpecification.colourDescription' in v:
            line['colour'] = v['vehicleSpecification']['colourDescription']
        else:
            line['colour'] = '-'
        if 'status.0.processName' in v:
            line['status'] = ['status'][0]['processName']
        else:
            line['status'] = '-'
        line['price'] = '0.00'
        output.append(line)
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

