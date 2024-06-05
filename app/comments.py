from flask import Blueprint, jsonify, request
from .db import get_db
from .config import Config
from bson.objectid import ObjectId
from datetime import datetime

comments_bp = Blueprint('comments', __name__)
db = get_db()
db_conn = db.comments

@comments_bp.route('/comments', methods=['POST'])
def create_comment():
    try:
        data = request.json
        movie_id = data.get('movie_id')
        comment = {
            "id": data.get('id'),
            "comment": data.get('comment'),
            "like": data.get('like', 0),
            "dislike": data.get('dislike', 0),
            "username": data.get('username'),
            "datetime": datetime.utcnow()
        }
        result = db_conn.update_one(
            {"movie_id": movie_id},
            {"$push": {"comments": comment}},
            upsert=True
        )
        return jsonify({"message": "Comment added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@comments_bp.route('/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    try:
        result = db_conn.find_one({"comments.id": int(comment_id)}, {"comments.$": 1})
        if result:
            return jsonify(result['comments'][0]), 200
        else:
            return jsonify({"error": "Comment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@comments_bp.route('/comments', methods=['GET'])
def get_comments():
    try:
        movie_id = request.args.get('movie_id')
        if movie_id:
            result = db_conn.find_one({"movie_id": movie_id})
            if result:
                return jsonify(result['comments']), 200
            else:
                return jsonify({"error": "No comments found for this movie"}), 404
        else:
            result = db_conn.find()
            comments_list = []
            for entry in result:
                comments_list.extend(entry['comments'])
            return jsonify(comments_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@comments_bp.route('/comments/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    try:
        data = request.json
        update_fields = {f"comments.$.{k}": v for k, v in data.items() if k in ["comment", "like", "dislike", "username"]}
        result = db_conn.update_one(
            {"comments.id": int(comment_id)},
            {"$set": update_fields}
        )
        if result.matched_count:
            return jsonify({"message": "Comment updated successfully"}), 200
        else:
            return jsonify({"error": "Comment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@comments_bp.route('/comments/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    try:
        result = db_conn.update_one(
            {"comments.id": int(comment_id)},
            {"$pull": {"comments": {"id": int(comment_id)}}}
        )
        if result.modified_count:
            return jsonify({"message": "Comment deleted successfully"}), 200
        else:
            return jsonify({"error": "Comment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
