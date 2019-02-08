from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask import render_template
from flask_login import LoginManager, UserMixin, login_required,login_user,logout_user
from user import User



app = Flask(__name__)

app.config['MONGO_DBNAME'] = "bims-uat"
app.config['MONGO_URI'] = "mongodb://localhost:27017/bims-uat"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mongo = PyMongo(app)

#Setup the login manager
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(userId):
    user = User()
    user.username = 'giles'
    user.password = 'password'
    return user


@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicle = mongo.db.vehicles
    output = []
    for v in vehicle.find(projection = {'regNo':1,
                                        'vehicleSpecification.manufacturer':1,
                                        'vehicleSpecification.colourDescription':1,
                                        'vehicleSpecification.model':1,
                                        'status.0.processName':1,
                                        'price.suggestedPrice':1}):
        line = {}
        line['regNo'] = v.get('regNo','-')
        vs = v['vehicleSpecification']
        line['manufacturer'] = vs.get('manufacturer', '-')
        line['model'] = vs.get('model','-')
        line['colour'] = vs.get('colourDescription', '-')
        if (v.get('status')):
            vss = v['status']
            vss0 = vss[0]
            line['status'] = vss0.get('processName','-')
        else:
            line['status'] = '-'
        if (v.get('price')):
            vp = v['price']
            line['price'] = vp.get('suggestedPrice', '0.00')
        else:
            line['price'] = '0.00'
        output.append(line)
    return render_template('vehicles.html', vehicles=output)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    user = User()
    user.username = 'giles'
    user.password = 'password'
    login_user(user, False)
    return render_template('login.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/view')
def view():
    vehicle = mongo.db.vehicles
    vehicle.getOne({})
    return 'Got Vehicle'

if __name__ == "__main__":
    app.run()

