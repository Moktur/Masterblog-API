"""modules providing functions to generate websites"""
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post",
        "content": "This is the first post."},
    {"id": 2, "title": "Second post",
        "content": "This is the second post."},
    {"id": 3, "title": "The Power of AI",
        "content": "Exploring how artificial \
        intelligence is transforming industries."},
    {"id": 4, "title": "Web Development Trends",
        "content": "Latest trends in web development for 2023."},
    {"id": 5, "title": "Healthy Living",
        "content": "Tips and tricks for lifestyle."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    provides all posts with and without any arguments.
    returns a new list, if sort != none and direction != asc, otherwise
    returns the untouched data.
    """
    sort_by = request.args.get('sort', None)
    direction = request.args.get('direction', 'asc')

    if sort_by is None:
        return jsonify(POSTS)

    if sort_by not in ['title', 'content']:
        return jsonify({"error": "Invalid sort parameter. \
            Use 'title' or 'content'."}), 400

    if direction not in ['asc', 'desc']:
        return jsonify({"error": "Invalid direction parameter. \
            Use 'asc' or 'desc'."}), 400

    sorted_posts = POSTS.copy()
    try:
        reverse_order = (direction.lower() == 'desc')
        sorted_posts.sort(key=lambda x: x[sort_by], reverse=reverse_order)
        return jsonify(sorted_posts)
    except Exception as e:
        return jsonify({"error": "Sorting failed", "details": str(e)}), 500


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post_by_id(post_id):
    """
    Deletes a post if found by id.
    Returns the deleted post.
    """
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404

    POSTS.remove(post)
    return jsonify(post)


@app.route('/api/posts', methods=['POST'])
def handle_posts():
    """
    User can upload a new post.
    Returns the new uploaded post.
    """
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400

        # if list of blogs is empty, new id will be 1
        if not POSTS:
            new_id = 1
        else:
            new_id = max(post['id'] for post in POSTS) + 1

        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_posts(post_id):
    """
    Update the title or content of a post if ID is provided.
    Returns the updated post.
    """
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": f"Post with ID {post_id} not found"}), 404

    new_data = request.get_json()
    post.update(new_data)
    return jsonify(post)


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """
    Searches the Blogs for the given content in both,
    title and content.
    Returns a list with the found posts.
    Returns an empty list if nothing was found.
    """
    title = request.args.get('title', "").lower()
    content = request.args.get('content', "").lower()
    posts_to_return = list()
    for post in POSTS:
        match_title = title in post['title'].lower()
        match_content = content in post['content'].lower()

        if (title and match_title) or (content and match_content):
            posts_to_return.append(post)
    if not posts_to_return:
        return jsonify(posts_to_return), 201
    else:
        return jsonify(posts_to_return), 201


def validate_post_data(data):
    """
    Helpermethod. validates if provided data has
    the fields "title" and "content".
    Returns Boolean
    """
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
