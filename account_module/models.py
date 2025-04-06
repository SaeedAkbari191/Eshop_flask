from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    avatar = db.Column(db.String(200), nullable=True)  # مسیر عکس پروفایل
    email_active_code = db.Column(db.String(100), nullable=False)
    about_user = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # مشابه فیلد active در جنگو
    is_superuser = db.Column(db.Boolean, default=False)  # فیلد سوپر یوزر برای مدیران
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # مشابه created_at در جنگو

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_admin(self):
        return self.is_superuser
