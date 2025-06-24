from flask import Blueprint, request, jsonify
from app.models.posts import Post
from app.extensions import db
from app.services.upload_utils import upload_media, sanitize_html

post_bp = Blueprint('post', __name__)
@post_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.Query.order_by(Post.created_at.desc()).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'image_urls': post.image_urls,
        'document_urls': post.document_urls,
        'created_at': post.created_at
    } for post in posts]), 200

@post_bp.route('/posts', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    admin_id = request.form.get('admin_id')

    if not all([title, content, admin_id]):
        return jsonify({'error': 'Missing required fields, Try again!'}), 400
    
    images = request.files.getlist('images')
    documents = request.files.getlist('documents')

    image_urls = upload_media(images, folder='funai_connect/images')
    document_urls = upload_media(documents, folder='funai_connect/docs')
    safe_content = sanitize_html(content)

    post = Post(
        title=title,
        content=safe_content,
        image_urls=image_urls,
        document_urls=document_urls,
        admin_id=admin_id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({'success': 'Post created successfully', 'post_id': post.id}), 201
@post_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'image_urls': post.image_urls,
        'document_urls': post.document_urls,
        'created_at': post.created_at
    }), 200