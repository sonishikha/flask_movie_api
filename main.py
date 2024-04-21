from flask import Flask, request, jsonify
from bson import Decimal128
import pymongo


app = Flask(__name__)

# Connection URI for MongoDB
mongo_uri = "mongodb+srv://dummy_project:uiFnFpWyRq02tucx@cluster0.eqfltw8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Function to convert Decimal128 to Python native types
def convert_decimal(value):
    if isinstance(value, Decimal128):
        return float(str(value))
    return value


def query_mongodb(id):
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)


        db = client["sample_airbnb"]
        collection = db["listingsAndReviews"]
        
        query = {"_id": id}
        print(id)

        # Execute the query
        results = list(collection.find(query))
        print(results)


        for doc in results:
            for key, value in doc.items():
                doc[key] = convert_decimal(value)

        return results

    except Exception as e:
        return {"error": str(e)}

@app.route('/query', methods=['GET'])
def query_api():
    # Get the parameter from the request
    id = request.args.get('id')

    # Check if id is provided
    if not id:
        return jsonify({"error": "Parameter is required."}), 400

    # Query the MongoDB database
    results = query_mongodb(id)


    return results


if __name__ == '__main__':
    app.run(debug=True)
