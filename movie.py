import pymongo

from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS
from bson.objectid import ObjectId


app = Flask(__name__)
cors = CORS(app)

# Connection URI for MongoDB
mongo_uri = "mongodb+srv://dummy_project:uiFnFpWyRq02tucx@cluster0.eqfltw8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client["sample_mflix"]
collection = db["movies"]


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/movies", methods = ["GET"])
def movies():
    try:
        response = []
        
        #pagination
        limit = int(request.args.get("limit", 10))
        page = int(request.args.get("page", 1))
        offset = (page-1)*limit

        # Execute the query
        pipeline = [
            {
                "$project": {
                    "id" : 1,
                    "title":1,
                    "imdb_rating" : "$imdb.rating",
                    "num_mflix_comments" : 1,  
                    "poster": {
                        "$cond": {
                            "if": {"$eq": [{"$type": "$poster"}, "missing"]},
                            "then": "",  # If 'poster' field is missing, project empty string
                            "else": "$poster"  # Otherwise, project the value of 'poster'
                        }
                    },
                    "released": {
                        "$cond": {
                            "if": {"$eq": [{"$type": "$released"}, "missing"]},
                            "then": "",  # If 'released' field is missing, project empty string
                            "else": "$released"  # Otherwise, project the value of 'released'
                        }
                    }
                }
            },
            {
                "$sort": {"_id": pymongo.ASCENDING}  # Sort by '_id' in ascending order
            },
            {
                "$skip": offset  # Skip 'offset' documents
            },
            {
                "$limit": limit  # Limit the number of documents to 'limit'
            }
        ]
        result = collection.aggregate(pipeline)

        for data in result:
            response.append({"id":str(data["_id"]), "title":data["title"], "released":data["released"], "imdb_rating":data["imdb_rating"], "no_of_comments":data["num_mflix_comments"], "poster":data["poster"]})

    except Exception as e:
        return {"error": str(e)}

    return jsonify(response)

@app.route('/movie/<string:movie_id>', methods=['GET'])
def movie(movie_id):
    try:
        response = []
        #Convert string movie_id to ObjectId
        object_id = ObjectId(movie_id)
        
        # Execute the query
        result = collection.find_one({"_id": object_id})
        if result:
            result['_id'] = str(result['_id'])
            response = result
        else:
            response = {"message":"No data found", "code":404, "status":"error"}
    except Exception as e:
        return {"error": str(e)}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8000)