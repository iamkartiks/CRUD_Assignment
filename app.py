from distutils.log import debug
from types import new_class
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from matplotlib.font_manager import json_dump
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '.uploaded_pics/'

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'demoDB'
app.config['MONGO_URI'] = 'mongodb+srv://iamkartiks:%40Arianna22@democluster.pzwws.mongodb.net/demoDB?retryWrites=true&w=majority'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

mongo = PyMongo(app)


recipe = mongo.db.demoConnection

@app.route('/', methods = ['GET'])
def get_all_routes():
    
    resp = jsonify(['All Recipes : http://127.0.0.1:5000/recipes', 'Specific Recipe : http://127.0.0.1:5000/recipe/<id>', 'Delete Recipe : http://127.0.0.1:5000/delete/<id>', 'Add Recipe : http://127.0.0.1:5000/add', 'Upload Pictures : http://127.0.0.1:5000/uploader'])


    return resp


@app.route('/recipes', methods=['GET'])
def get_all_recipes():

    output = []
    for q in recipe.find():
        output.append({'recipe_name' : q['recipe_name'], 'Instructions' : q['Instructions'], 'Ingredients' : q['Ingredients'], 'Items': q['Items']})

    return jsonify({'result' : output})

# ADD A NEW OBJECT

@app.route('/add', methods=['POST'])
def add_recipe():
    recipe = mongo.db.demoConnection

    recipe_name = request.get_json['recipe_name']
    Instructions = request.get_json['Instructions']
    Ingredients = request.get_json['Ingredients']
    Items = request.get_json['Items'] 

    if request.method == 'POST':
        recipe_id = recipe.insert({'recipe_name':recipe_name, 'Instructions':Instructions, 'Ingredients':Ingredients,'Items':Items })
        new_recipe = recipe.find_one({'_id':recipe_id})

        output = {'recipe_name':new_recipe['recipe_name'], 'Instructions':new_recipe['Instructions'], 'Ingredients':new_recipe['Ingredients'],'Items':new_recipe['Items']}

    return jsonify({'result':output})

# UPLOAD IMAGES
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            resp = jsonify('No file part')
            return resp
        file = request.files['file']
        
        if file.filename == '':
            resp = jsonify('No selected file')
            return resp
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resp = jsonify('Image successfully uploaded and displayed below')
            return resp
        else:
            resp = jsonify('Allowed image types are -> png, jpg, jpeg, gif')
            return resp

# GET OBJECT BY ID

@app.route('/recipe/<_id>', methods=['GET'])
def get_recipe(_id):

    recipe=mongo.db.demoConnection

    q = recipe.find_one({'_id':ObjectId(_id)})

    if q:
        output = {'recipe_name':q['recipe_name'], 'Instructions':q['Instructions'], 'Ingredients':q['Ingredients'],'Items':q['Items']}
    else:
        output = "No Results Found"

    return jsonify({'result':output})


# DELETE OBJECT

@app.route('/delete/<id>', methods=['DELETE'])
def delete_recipe(id):
    recipe.delete_one({'_id' : ObjectId(id)})
    return jsonify("Successfully Deleted !")



# UPDATE OBJECT

@app.route('/update/<id>',methods=['PUT'])
def update_recipe(id):
    recipe=mongo.db.demoConnection

    _json = request.json
    recipe = recipe.query.get(id)
    recipe_name = _json['recipe_name']
    Ingredients = _json['Ingredients']
    Instructions = _json['Instructions']
    Items = _json['Items']
    
    if  id and request.method == 'PUT':

        mongo.db.user.update_one({'_id': ObjectId(id['id']) if 'id' in id else ObjectId(id)}, {'$set': {'recipe_name': recipe_name, 'Ingredients': Ingredients, 'Instructions': Instructions, 'Items':Items}})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp



if __name__ == "__main__":
    app.run(debug=True)