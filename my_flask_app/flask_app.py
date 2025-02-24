from flask import Flask, request, jsonify
import requests
import os
from supabase import create_client, Client

app = Flask(__name__)

# Supabase configuration (replace with your actual credentials)
SUPABASE_URL = os.environ.get("SUPABASE_URL")  # Get from environment variables
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") # Get from environment variables
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Table name in Supabase (create this table beforehand)
TABLE_NAME = "posts"  # Matches the structure of jsonplaceholder.typicode.com/posts

@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        data = supabase.table(TABLE_NAME).select("*").execute()
        posts = data.data
        return jsonify(posts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts', methods=['POST'])
def create_post():
    try:
        new_post = request.get_json()

        # Validate the incoming data (important!)
        required_fields = ["userId", "title", "body"] # Matches jsonplaceholder.typicode.com/posts
        if not all(field in new_post for field in required_fields):
          return jsonify({"error": "Missing required fields"}), 400

        data = supabase.table(TABLE_NAME).insert(new_post).execute()
        created_post = data.data[0] # The inserted data is returned
        return jsonify(created_post), 201  # 201 Created

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        updated_post = request.get_json()

         # Validate the incoming data (important!)
        required_fields = ["userId", "title", "body"] # Matches jsonplaceholder.typicode.com/posts
        if not all(field in updated_post for field in required_fields):
          return jsonify({"error": "Missing required fields"}), 400


        data = supabase.table(TABLE_NAME).update(updated_post).eq("id", post_id).execute()
        if data.data: # Check if a record was actually updated
          updated_post_data = data.data[0]
          return jsonify(updated_post_data), 200
        else:
          return jsonify({"message": "Post not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        data = supabase.table(TABLE_NAME).delete().eq("id", post_id).execute()
        if data.data: # Check if a record was actually deleted
          return jsonify({"message": "Post deleted"}), 204 # 204 No Content
        else:
          return jsonify({"message": "Post not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production on PythonAnywhere