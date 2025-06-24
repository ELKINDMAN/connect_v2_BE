from flask_mail import Message
from datetime import datetime, timedelta
from app.extensions import mail, db

def generate_reset_token(admin):
    import secrets
    token = secrets.token_urlsafe(32)
    admin.reset_token = token
    admin.reset_token_expiry = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()
    return f'http://localhost:5000/reset_password/{token}'

def send_reset_email(email, url):
    msg = Message(
        subject='Password Reset Request',
        sender='no-reply@funai-connect.com',
        recipients=[email]
    )
    msg.html = f'<p>Click the link to reset your password:</p><a href="{url}">{url}</a>'
    mail.send(msg)
    return True
