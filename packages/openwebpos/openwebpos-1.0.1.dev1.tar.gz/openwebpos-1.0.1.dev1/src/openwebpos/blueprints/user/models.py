from datetime import datetime

from flask_login import UserMixin
from usernames import is_safe_username
from werkzeug.security import generate_password_hash, check_password_hash

from openwebpos.extensions import db
from openwebpos.utils.sql import DateTimeMixin, CRUDMixin


class User(UserMixin, DateTimeMixin, CRUDMixin, db.Model):
    """
    User model for defining users.
    """
    __tablename__ = "user"

    # Authentication
    username = db.Column(db.String(120), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(120), nullable=False, server_default='')
    pin = db.Column(db.String(10))
    staff = db.Column(db.Boolean, default=False, nullable=False,
                      server_default='0')
    admin = db.Column(db.Boolean, default=False, nullable=False,
                      server_default='0')
    active = db.Column('is_active', db.Boolean(), nullable=False,
                       server_default='1')

    # One-to-One relationships
    profile = db.relationship('UserProfile', backref='user', lazy=True,
                              uselist=False)
    activity = db.relationship('UserActivity', backref='user', lazy=True,
                               uselist=False)

    @staticmethod
    def insert_user():
        """
        Insert default user in the database.
        """
        user = User(username='admin',
                    email='admin@mail.com',
                    password=generate_password_hash('admin'),
                    pin='1234')
        user.save()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def set_password(self, password):
        """
        Set user password.

        Args:
            password (str): Password to set.

        Returns:
            None
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the password is correct.

        Args:
            password (str): Password to check.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return check_password_hash(password, self.password)

    def check_if_safe_username(self):
        return is_safe_username(self.username)

    def is_active(self):
        """
        Return whether user account is active.

        Returns:
            bool: True if user account is active, False otherwise.
        """
        return self.active

    def is_admin(self):
        """
        Return whether user is admin.

        Returns:
            bool: True if user is admin, False otherwise.
        """
        return self.admin

    def is_staff(self):
        """
        Return whether user is staff.

        Returns:
            bool: True if user is staff, False otherwise.
        """
        return self.staff


class UserProfile(DateTimeMixin, CRUDMixin, db.Model):
    """
    User profile model.
    """
    __tablename__ = "user_profile"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    picture = db.Column(db.String(255), nullable=True, default='default.png')
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip_code = db.Column(db.String(120))
    dob = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(UserProfile, self).__init__(**kwargs)


class UserActivity(CRUDMixin, db.Model):
    """
    User activity model.
    """
    __tablename__ = "user_activity"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime, nullable=True)
    current_sign_in_ip = db.Column(db.String(100), nullable=True)
    last_sign_in_at = db.Column(db.DateTime, nullable=True)
    last_sign_in_ip = db.Column(db.String(100), nullable=True)
    user_agent = db.Column(db.String(120))
    referrer = db.Column(db.String(120))

    def __init__(self, **kwargs):
        super(UserActivity, self).__init__(**kwargs)

    def update_activity(self, ip_address: str, user_id: int):
        """
        Update the fields associated with user activity tracking.

        Args:
            ip_address: IP address of the user.
            user_id: ID of the user.

        Returns:
            None
        """
        self.user_id = user_id
        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_at = datetime.utcnow()
        self.current_sign_in_ip = ip_address
        if self.sign_in_count is None:
            self.sign_in_count = 1
        else:
            self.sign_in_count += 1

        return self.save()
