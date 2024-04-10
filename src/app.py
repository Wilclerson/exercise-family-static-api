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
    if members:
        response_body = {
            "family": members
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"message": "Members not found"}), 404
    
@app.route('/member', methods=['POST'])
def handle_add():
    new_member = request.json
    if new_member:
        added_member = jackson_family.add_member(new_member)
        response_body = {
            "member": added_member
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"message": "New member not found"}), 404

@app.route('/member/<int:id>', methods=['GET'])
def handle_get_specific_member(id):
    member = jackson_family.get_member(id)
    if member:
        response_body = {
            "name": f"{member['first_name']} {member['last_name']}",
            "id": member['id'],
            "age": member['age'],
            "lucky_numbers": member['lucky_numbers']
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"message": "Member not found"}), 404

    

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete_member(id):
    member = jackson_family.delete_member(id)
    if member:
        response_body = {
            "done": True
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"message": "Member not found"}), 404
    

    




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)