import pymongo

from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS


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
        request_data = request.args.get("limit")
        print(request_data)
        response = []
        
        #pagination
        limit = 10
        if request_data["limit"] != "":
            limit = request_data["limit"]
        page = 1
        if request_data["page"] != "":
            page = request_data["page"]
        offset = (page-1)*limit

        # Execute the query
        result = collection.find({}).sort('_id', pymongo.ASCENDING).skip(offset).limit(limit)
        for data in result:
            response.append({"title":data["title"], "released":data["released"], "imdb_rating":data["imdb"]['rating'], "no_of_comments":data["num_mflix_comments"], "poster":[]})

    except Exception as e:
        return {"error": str(e)}

    return jsonify(response)

@app.route('/movie/<int:movie_id>')
def show_post(movie_id):
    # show the post with the given id, the id is an integer
    return f'Post {movie_id}'

if __name__ == '__main__':
    app.run(debug=True, port=8000)