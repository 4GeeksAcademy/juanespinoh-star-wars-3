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
from models import db, User,People,Planet,Nave
from sqlalchemy import select
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
# ********USERS ROUTES************
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"msg": "falta name"}), 400
    
    new_user = User(name=data['name'])
    
    try:
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "msg": "Usuario creado exitosamente"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear usuario: {str(e)}"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        all_people = db.session.execute(
            select(User).order_by(User.id)
        ).scalars().all()


        people_list = [person.serialize() for person in all_people]

        return jsonify({
            "result": people_list
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener usuarios: {str(e)}"
        }), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_to_delete = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()


        if not user_to_delete:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        db.session.delete(user_to_delete)
        db.session.commit()

        return jsonify({
            "msg": "Usuario eliminado exitosamente"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener usuarios: {str(e)}"
        }), 500

# **********PEOPLE ROUTES ***********
@app.route('/people', methods=['POST'])
def add_people():
    data = request.get_json()
    print(data)
    
    if not data or 'name' not in data or 'birth_year' not in data or 'gender' not in data or 'hair_color' not in data:
        return jsonify({"msg": "campos por llenar"}), 400
    
    new_person = People(name=data['name'], birth_year=data["birth_year"],gender=data["gender"],hair_color=data["hair_color"])
    
    try:
        db.session.add(new_person)
        db.session.commit()
        
        return jsonify({
            "msg": "Persona creado exitosamente"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear usuario: {str(e)}"}), 500

@app.route('/people', methods=['GET'])
def get_people():
    try:
        all_people = db.session.execute(
            select(People).order_by(People.id)
        ).scalars().all()


        person_list = [person.serialize() for person in all_people]

        return jsonify({
            "result": person_list
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener persons: {str(e)}"
        }), 500

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    try:
        people_to_delete = db.session.execute(
            select(People).where(People.id==people_id)
        ).scalars().first()


        if not people_to_delete:
            return jsonify({"msg": "Persona no encontrada"}), 404
        
        db.session.delete(people_to_delete)
        db.session.commit()

        return jsonify({
            "msg": "Persona eliminado exitosamente"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener Persona: {str(e)}"
        }), 500

# **********PLANETAS ROUTES ***********
@app.route('/planets', methods=['POST'])
def add_planet():
    data = request.get_json()
 
    
    if not data or 'name' not in data or 'climate' not in data or 'gravity' not in data or 'population' not in data:
        return jsonify({"msg": "campos por llenar"}), 400
    
    new_planet = Planet(name=data['name'], climate=data["climate"],gravity=data["gravity"],population=data["population"])
    
    try:
        db.session.add(new_planet)
        db.session.commit()
        
        return jsonify({
            "msg": "Planeta creado exitosamente"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear usplanetauario: {str(e)}"}), 500

@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        all_planets = db.session.execute(
            select(Planet).order_by(Planet.id)
        ).scalars().all()


        planets_list = [planet.serialize() for planet in all_planets]

        return jsonify({
            "result": planets_list
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener planets: {str(e)}"
        }), 500

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    try:
        planet_to_delete = db.session.execute(
            select(Planet).where(Planet.id==planet_id)
        ).scalars().first()


        if not planet_to_delete:
            return jsonify({"msg": "Persona no encontrada"}), 404
        
        db.session.delete(planet_to_delete)
        db.session.commit()

        return jsonify({
            "msg": "Planeta eliminado exitosamente"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al eliminar Planeta: {str(e)}"
        }), 500

# **********NAVES ROUTES**********
@app.route('/naves', methods=['POST'])
def add_nave():
    data = request.get_json()
 
    
    if not data or 'name' not in data or 'cargo_capacity' not in data or 'crew' not in data or 'model' not in data:
        return jsonify({"msg": "campos por llenar"}), 400
    
    new_nave = Nave(name=data['name'], cargo_capacity=data["cargo_capacity"],crew=data["crew"],model=data["model"])
    
    try:
        db.session.add(new_nave)
        db.session.commit()
        
        return jsonify({
            "msg": "Nave creado exitosamente"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error al crear nave: {str(e)}"}), 500

@app.route('/naves', methods=['GET'])
def get_naves():
    try:
        all_naves = db.session.execute(
            select(Nave).order_by(Nave.id)
        ).scalars().all()


        all_naves = [nave.serialize() for nave in all_naves]

        return jsonify({
            "result": all_naves
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener naves: {str(e)}"
        }), 500

@app.route('/naves/<int:nave_id>', methods=['DELETE'])
def delete_naves(nave_id):
    try:
        nave_to_delete = db.session.execute(
            select(Nave).where(Nave.id==nave_id)
        ).scalars().first()


        if not nave_to_delete:
            return jsonify({"msg": "Persona no encontrada"}), 404
        
        db.session.delete(nave_to_delete)
        db.session.commit()

        return jsonify({
            "msg": "Nave eliminada exitosamente"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al eliminar Nave: {str(e)}"
        }), 500


# PARA LAS RUTAS DE FAVORITOS SE PASA user_id POR BODY
# **********ADD PEOPLE FAVORITES**********
@app.route("/favorite/people/<int:people_id>",methods=["POST"])
def add_person_favorites(people_id):
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()
     

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        person = db.session.execute(
            select(People).where(People.id==people_id)
        ).scalars().first()

        if not person:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        
        if person in user.people_favoritos:
            return jsonify({"msg": "Planeta ya agregado"}), 404
        
        user.people_favoritos.append(person)
        db.session.commit()

        return jsonify({
            "msg": "agregado"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener usuarios: {str(e)}"
        }), 500

@app.route("/favorite/people/<int:people_id>",methods=["DELETE"])
def delete_person_favorites(people_id):
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()
     

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        person = db.session.execute(
            select(People).where(People.id==people_id)
        ).scalars().first()

        if not person:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        
        user.people_favoritos.remove(person)
        db.session.commit()

      

        return jsonify({
            "msg": "Planeta  eliminado exitosamente de favoritos"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener usuarios: {str(e)}"
        }), 500
    
@app.route("/users/favorites",methods=["GET"])
def get_favorites():
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        people_favoritos = [people.serialize() for people in user.people_favoritos]
        planetas_favoritos = [planet.serialize() for planet in user.planetas_favoritos]
        naves_favoritos = [nave.serialize() for nave in user.naves_favoritos]
        

        return jsonify({
            "resultado":{
                "people_favoritos":people_favoritos,
                "planetas_favoritos":planetas_favoritos,
                "naves_favoritos":naves_favoritos
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener favoritos: {str(e)}"
        }), 500


# **********ADD PLANETAS FAVORITES**********
@app.route("/favorite/planet/<int:planet_id>",methods=["POST"])
def add_planet_favorites(planet_id):
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()
     

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        planet = db.session.execute(
            select(Planet).where(Planet.id==planet_id)
        ).scalars().first()

        if not planet:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        
        if planet in user.planetas_favoritos:
            return jsonify({"msg": "Planeta ya agregado"}), 404
        
        user.planetas_favoritos.append(planet)
        db.session.commit()

        return jsonify({
            "msg": "agregado"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al agregar a favoritos: {str(e)}"
        }), 500

@app.route("/favorite/planet/<int:planet_id>",methods=["DELETE"])
def delete_planet_favorites(planet_id):
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()
     

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        planet = db.session.execute(
            select(Planet).where(Planet.id==planet_id)
        ).scalars().first()

    

        if not planet:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        
        user.planetas_favoritos.remove(planet)
        db.session.commit()

      

        return jsonify({
            "msg": "Planeta  eliminado exitosamente de favoritos"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al obtener usuarios: {str(e)}"
        }), 500

# **********ADD NAVES FAVORITES**********
@app.route("/favorite/nave/<int:nave_id>",methods=["POST"])
def add_nave_favorites(nave_id):
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()
     

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        nave = db.session.execute(
            select(Nave).where(Nave.id==nave_id)
        ).scalars().first()

        if not nave:
            return jsonify({"msg": "Nave no encontrado"}), 404
        
        if nave in user.naves_favoritos:
            return jsonify({"msg": "Nave ya agregado"}), 404
        
        user.naves_favoritos.append(nave)
        db.session.commit()

        return jsonify({
            "msg": "agregado"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al agregar a favoritos: {str(e)}"
        }), 500
    
@app.route("/favorite/nave/<int:nave_id>",methods=["DELETE"])
def delete_nave_favorites(nave_id):
    user_id = request.get_json()["user_id"]

    try:
        if not user_id:
            return jsonify({"msg": "No hay id de usuario"}), 404

        user = db.session.execute(
            select(User).where(User.id==user_id)
        ).scalars().first()
     

        if not user:
            return jsonify({"msg": "Usuario no encontrado"}), 404
        
        nave = db.session.execute(
            select(Nave).where(Nave.id==nave_id)
        ).scalars().first()

    

        if not nave:
            return jsonify({"msg": "Planeta no encontrado"}), 404
        
        user.naves_favoritos.remove(nave)
        db.session.commit()

      

        return jsonify({
            "msg": "Nave  eliminado exitosamente de favoritos"
        }), 200
    
    except Exception as e:
        return jsonify({
            "msg": f"Error al eliminar nave de favoritos: {str(e)}"
        }), 500
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
