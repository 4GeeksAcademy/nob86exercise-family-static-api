"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def handle_hello2(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member_id), 200
    else:
        return jsonify({"msg": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json()
    # if not new_member or 'first_name' not in new_member or 'age' not in new_member or 'lucky numbers' in new_member:
    #     return jsonify({"msg": "first_name and age are required"}), 400
    id_member = jackson_family._generateId()
    new_member = {
        "id": id_member,
        "first_name": body['first_name'],
        "last_name": jackson_family.last_name
        "age": body['age'],
        "lucky numbers": body['lucky numbers'],      
    }
    jackson_family.add_member(new_member)
    return jsonify({"msg": "Member added successfully"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result:
        return jsonify({"msg": "Member deleted successfully"}), 200
    else:
        return jsonify({"msg": "Member not found"}), 404
  
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
