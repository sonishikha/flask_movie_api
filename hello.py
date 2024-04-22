from flask import Flask, render_template
import pymongo

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

# Connection URI for MongoDB
mongo_uri = "mongodb+srv://dummy_project:uiFnFpWyRq02tucx@cluster0.eqfltw8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@app.route("/movies")
def movies():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)

        db = client["sample_mflix"]
        collection = db["movies"]

        # Execute the query
        results = list(collection.find({}).limit(10))

    except Exception as e:
        return {"error": str(e)}

    return results

@app.route('/movie/<int:movie_id>')
def show_post(movie_id):
    # show the post with the given id, the id is an integer
    return f'Post {movie_id}'

if __name__ == '__main__':
    app.run(debug=True, port=8000)