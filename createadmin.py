# create_admin.py
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin_email = 'admin@admin.com'
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            username='Admin',
            email=admin_email,
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully.")
    else:
        print("⚠️ Admin user already exists.")
