from flask import request, Flask, jsonify
from pymongo.mongo_client import MongoClient
from flask_cors import CORS
uri = "mongodb+srv://shopmongo:1212312121@cluster0.kjvosuu.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri)

app = Flask(__name__)
CORS(app)

db = client["shop"]
collection = db["shop_info"]

@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/shop", methods=["GET"])
def get_all_shop():
    data = collection.find()
    return jsonify(list(data))

@app.route("/shop/<int:product_id>", methods=["GET"])
def get_student(product_id):
    product = collection.find_one({"_id": product_id})
    if product:
        return jsonify(product)
    else:
        return jsonify({"error": "product not found"}), 404
    
@app.route("/shop", methods=["POST"])
def create_product():
    new_data = request.json
    collection.insert_one(new_data)
    return jsonify(new_data), 201

@app.route("/shop/<string:product_id>", methods=["PUT"])
def update_student(product_id):
    print(f"Updating product with ID: {product_id}")

    product = collection.find_one({"_id": product_id})
    if product:
        data = request.json
        collection.update_one({"_id": product_id}, {"$set": data})
        updated_student = collection.find_one({"_id": product_id})
        return jsonify(updated_student)
    else:
        return jsonify({"error": "product not found"}), 404

@app.route("/shop/<string:product_id>", methods=["DELETE"])
def student_delete(product_id):
    product = collection.find_one({"_id": product_id})
    if product:
        collection.delete_one({"_id": product_id})
        return jsonify({"message": "product deleted successfully"}), 200
    else:
        return jsonify({"error": "product not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
