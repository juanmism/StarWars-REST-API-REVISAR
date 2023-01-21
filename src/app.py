"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET']) #PREGUNTAR TUTORÍA
def user_list():
    user = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("user/list.html", user=user)

@app.route('/user/<user_id>', methods=['GET'])
def handle_user_ids(user_id):
    print(user_id)
    user = User.query.get(user_id)
    print(user)
    return jsonify(user.serialize()), 200

@app.route('/user/register', methods=['POST'])
def create_user():
    body = request.get_json()
    new_user = User(email=body['email'], password=body['password'], is_active= True) 
    print(new_user)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 200


@app.route('/planet', methods=['GET']) #PREGUNTAR TUTORÍA
def planet_list():
    planet = db.session.execute(db.select(Planet).order_by(planet.id)).scalars()
    return render_template("planet/list.html", planet=planet)


@app.route('/planet/<planet_id>', methods=['GET'])
def handle_planet_ids(planet_id):
    print(planet_id)
    planet = Planet.query.get(planet_id)
    print(planet)
    return jsonify(planet.serialize()), 200

  

@app.route('/planet/register', methods=['POST'])
def create_planet():
    body = request.get_json()
    new_planet = Planet(planet_name=body['planet_name'], planet_climate=body['planet_climate']) 
    print(new_planet)
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
