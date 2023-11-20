from flask import jsonify, request


blog_posts = []  


# def get_posts():
#     try:
#         return jsonify({'posts': blog_posts}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


def get_post(id):
    try:
        # Find the post with the given ID
        post = next((post for post in blog_posts if post['id'] == id), None)
        if post:
            return jsonify({'post': post}), 200
        else:
            return jsonify({'error': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_post(id):
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        # Find the post with the given ID
        post = next((post for post in blog_posts if post['id'] == id), None)

        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Update the post with the new data
        post['title'] = title
        post['content'] = content
        return jsonify({'message': 'Blog post updated', 'post': post}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
