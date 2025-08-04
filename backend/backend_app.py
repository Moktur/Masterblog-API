from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post_by_id(id):
    if request.method == 'DELETE':
        post = find_post_by_id(id)
        if post is None:
             return '', 404
        POSTS.remove(post)
        return jsonify(post)


@app.route('/api/posts', methods=['POST'])
def handle_posts():
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400
        
        # generate post ID
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id
        # Add the new post
        POSTS.append(new_post)
        #return the new post to the client
        return jsonify(new_post), 201


def validate_post_data(data):
    return 'title' in data and 'content' in data


def find_post_by_id(post_id):
	"""Find the post with the id `post_id`.
	If there is no post with this id, return None."""
	for post in POSTS:
		if post['id'] == post_id:
			return post
	return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
