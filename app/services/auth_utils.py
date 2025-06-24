from app.extensions import db
from app.models.admin import Admin
from datetime import datetime

def authenticate_admin(username_or_email, password):
    admin = Admin.query.filter(
        (Admin.username == username_or_email) | (Admin.email == username_or_email)
    ).first()
    if admin and admin.check_password(password):
        admin.last_login = datetime.utcnow()
        admin.login_count = (admin.login_count or 0) + 1
        db.session.commit()
        return admin
    return None

def get_admin_by_id(admin_id):
    return Admin.query.get(admin_id)