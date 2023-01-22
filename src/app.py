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
from models import db, User, Planet, Favorite, People
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

# USER
@app.route('/user', methods=['GET']) 
def user_list():
    all_users = User.query.all()
    print(all_users)
    usuarios = list( map ( lambda user: user.serialize(), all_users))
    return jsonify(usuarios)

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

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user_ids(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({ "delete user ": user }), 200

# PEOPLE
@app.route('/people', methods=['GET']) 
def people_list():
    all_people = People.query.all()
    print(all_people)
    personas = list( map ( lambda people: people.serialize(), all_people))
    return jsonify(personas)


@app.route('/people/<people_id>', methods=['GET'])
def handle_people_ids(people_id):
    print(people_id)
    people = People.query.get(people_id)
    print(people)
    return jsonify(people.serialize()), 200

@app.route('/people/register', methods=['POST'])
def create_people():
    body = request.get_json()
    new_people = People(name=body['name'], height=body['height'], hair=body['hair'], eyes=body['eyes'], birth=body['birth'], gender=body["gender"] )
    print(new_people)
    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 200

# PLANETS

@app.route('/planet', methods=['GET']) 
def user_planet():
    all_planet = Planet.query.all()
    print(all_planet)
    planetas = list( map ( lambda planet: planet.serialize(), all_planet))
    return jsonify(planetas)

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

@app.route('/planet/<planet_id>', methods= ['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()
    return jsonify({ "delete planet ": planet })

# FAVORITE
@app.route('/favorite', methods=['GET']) 
def favorite_list():
    all_favorite = Favorite.query.all()
    print(all_favorite)
    favoritos = list( map ( lambda favorite: favorite.serialize(), all_favorite))
    return jsonify(favoritos)

@app.route('/favorite/<favorite_id>', methods=['GET'])
def handle_favorite_ids(favorite_id):
    print(favorite_id)
    favorite = Favorite.query.get(favorite_id)
    print(favorite)
    return jsonify(favorite.serialize()), 200

# ERROR CUANDO ENVIO DESDE POSTMAN - POST: raise TypeError(f"Object of type {type(o).__name__} 
#   is not JSON serializable")
#   TypeError: Object of type People is not JSON serializable
@app.route('/favorite/register', methods=['POST'])
def create_favorite():
    body = request.get_json()
    new_favorite = Favorite(favorite_user_id=body['favorite_user_id'], favorite_people_id=body['favorite_people_id'], favorite_planet_id=body['favorite_planet_id'])
    print(new_favorite)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
