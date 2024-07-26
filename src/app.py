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
from models import db, User, Planet, People, People_favorites, Planet_Favorites
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

@app.route('/user/', methods=['GET'])
def list_user():
    users_query=User.query.all() 
    users_list=list(map(lambda user:user.serialize(),users_query))
    return jsonify(users_list)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    is_active = data.get('is_active', True)  # Valor por defecto True

    if not first_name or not last_name or not email or not password:
        return jsonify({'error': 'Missing data'}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=hashed_password,
        is_active=is_active
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201
    
@app.route('/people', methods=['GET'])
def get_all_people():
    people_query = People.query.all()
    people_list = list(map(lambda people: people.serialize(), people_query))
    return jsonify(people_list)

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    person = People.query.filter_by(id=people_id).first()
    if person is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(person.serialize())

# endpoind planetas

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets_query = Planet.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), planets_query))
    return jsonify(planets_list)

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(planet.serialize())

@app.route('/users/favorites/', methods=['GET'])
def get_all_favorites():
    user_query = User.query.first()
    people_favorite_query = People_favorites.query.filter_by(user_id=user_query.id).all()
    planet_favorite_query = Planet_Favorites.query.filter_by(user_id=user_query.id).all()
    people_favorites_list = list(map(lambda favorite:favorite.serialize(), people_favorite_query))
    favorites_planets_list=list(map(lambda favorite:favorite.serialize(), planet_favorite_query))    
    
    return jsonify({
        "people": people_favorites_list,
        "planet": favorites_planets_list})


@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    favorite_planet = Planet_Favorites(user=user, planet=planet)
    db.session.add(favorite_planet)
    db.session.commit()
    return jsonify({"info": "Favorite added"})

@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_People_favorites(user_id, people_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    people = People.query.filter_by(id=people_id).first()
    if people is None:
        return jsonify({"error": "people not found"}), 404
    
    people_favorites = People_favorites(user=user, people=people)
    db.session.add(people_favorites)
    db.session.commit()
    return jsonify({"info": "Favorite people added"})

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    favorite_planet = Planet_Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404
    
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({"info": "Favorite planet deleted"})


@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_People_favorites(user_id, people_id):
    if user_id is None or user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    people_favorites = People_favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if people_favorites is None:
        return jsonify({"error": "Favorite people not found"}), 404
    
    db.session.delete(people_favorites)
    db.session.commit()
    return jsonify({"info": "Favorite people deleted"})





# @app.route('/users/favorites', methods=['GET'])
# def get_user_favorites():
#     user_id = request.args.get('user_id')

#     if not user_id:
#         return jsonify({"error": "user_id is required"}), 400

#     people_favorites = People_favorites.query.filter_by(user_id=user_id).all()
#     planet_favorites = Planet_Favorites.query.filter_by(user_id=user_id).all()

#     people_fav_list = [{"id": fav.id, "first_name": fav.first_name} for fav in people_favorites]
#     planet_fav_list = [{"id": fav.id, "name": fav.name} for fav in planet_favorites]

#     return jsonify({"people_favorites": people_fav_list, "planet_favorites": planet_fav_list})




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
