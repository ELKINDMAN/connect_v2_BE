from app.extensions import db
from app.models.admin import Admin
from app.models.posts import Post


def print_all_admins_and_posts():
    admins = Admin.query.all()
    posts = Post.query.all()

    if not admins:
        print('No admins found.')
    else:
        print('Admins:')
        for admin in admins:
            print(f"ID: {admin.id}, Name: {admin.name}, Username: {admin.username}, Email: {admin.email}")

    if not posts:
        print('No posts found.')
    else:
        print('\nPosts:')
        for post in posts:
            print(f"ID: {post.id}, Title: {post.title}, Author ID: {post.admin_id}, Created At: {post.created_at}")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        print_all_admins_and_posts()
