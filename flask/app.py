from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost:27017/demo2'
mongo = PyMongo(app)

CORS(app)
db = mongo.db.demo2

@app.route('/', methods=["GET", "POST"])
def getpost():
    if request.method == "GET":
        o = []
        for i in db.find():
            o.append({
                "_ID": str(i["_id"]),
                "name": i["name"],
                "email": i["email"],
                "password": i["password"]
            })
        return jsonify(o)

    elif request.method == "POST":
        result = db.insert_one({
            "name": request.json["name"],
            "email": request.json["email"],
            "password": request.json["password"]
        })
        return jsonify({"_ID": str(result.inserted_id)})

@app.route('/<id>', methods=["DELETE", "PUT"])
def deleteput(id):
    if request.method == "DELETE":
        db.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "deleted"})
    elif request.method == "PUT":
        db.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.json["name"],
                "email": request.json["email"],
                "password": request.json["password"]
            }}
        )
        return jsonify({"message": "updated"})

@app.route('/getone/<id>', methods=["GET"])
def getone(id):
    res = db.find_one({"_id": ObjectId(id)})
    if res:
        return jsonify({
            "_ID": str(res["_id"]),
            "name": res["name"],
            "email": res["email"],
            "password": res["password"]
        })
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
