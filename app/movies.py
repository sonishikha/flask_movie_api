from flask import Blueprint, jsonify, request
from .db import get_db
from bson.objectid import ObjectId
from .config import Config

movies_bp = Blueprint('movies', __name__)
db = get_db()
db_conn = db.movies

@movies_bp.route("/movies", methods = ["GET"])
def get_movies():
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
                "$sort": {"_id": 1}  # Sort by '_id' in ascending order
            },
            {
                "$skip": offset  # Skip 'offset' documents
            },
            {
                "$limit": limit  # Limit the number of documents to 'limit'
            }
        ]
        result = db_conn.aggregate(pipeline)

        for data in result:
            response.append({"id":str(data["_id"]), "title":data["title"], "released":data["released"], "imdb_rating":data["imdb_rating"], "no_of_comments":data["num_mflix_comments"], "poster":data["poster"]})

    except Exception as e:
        return {"error": str(e)}

    return jsonify(response)

@movies_bp.route('/movies/<string:movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        response = []
        #Convert string movie_id to ObjectId
        object_id = ObjectId(movie_id)
        
        # Execute the query
        result = db_conn.find_one({"_id": object_id})
        if result:
            result['_id'] = str(result['_id'])
            response = result
        else:
            response = {"message":"No data found", "code":404, "status":"error"}
    except Exception as e:
        return {"error": str(e)}
    
    return jsonify(response)

@movies_bp.route("/genres", methods=["GET"])
def get_genres():
    try:
        pipeline = [
            {"$unwind": "$genres"},
            {"$group": {"_id": {"genres": "$genres"}, "count": {"$sum": 1}}}
        ]
        result = db_conn.aggregate(pipeline)
        response = []
        
        if result:
            for entry in result:
                response.append({"genres": str(entry["_id"]["genres"]), "count": int(entry["count"])})
        else:
            response = {"message": "No data found", "code": 404, "status": "error"}

    except Exception as e:
        return {"error": str(e)}
    
    return jsonify(response)


@movies_bp.route("/languages", methods=["GET"])
def get_languages():
    try:
        pipeline = [
            {"$unwind": "$languages"},
            {"$group": {"_id": {"languages": "$languages"}, "count": {"$sum": 1}}}
        ]
        
        result = db_conn.aggregate(pipeline)
        response = []
        
        if result:
            for entry in result:
                response.append({"languages": str(entry["_id"]["languages"]), "count": int(entry["count"])})
        else:
            response = {"message": "No data found", "code": 404, "status": "error"}

    except Exception as e:
        return {"error": str(e)}
    
    return jsonify(response)
