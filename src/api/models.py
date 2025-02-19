from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

# Initialize database
db = SQLAlchemy()


# Models


# Enums
class UserRole(Enum):
    ADMIN = "Admin"
    USER = "User"
    GUEST = "Guest"
    GROWER = "Grower"
    DISPENSARY_OWNER = "Dispensary Owner"
    BUDTENDER = "Budtender"
    LEGAL_ADVISOR = "Legal Advisor"
    CUSTOMER = "Customer"
    OTHER = "Other"

class InterestCategory(Enum):
    CULTIVATION = 'Cultivation'
    DISPENSARY_MANAGEMENT = 'Dispensary Management'
    CANNABIS_LAW = 'Cannabis Law'
    PRODUCT_DEVELOPMENT = 'Product Development'
    MARKETING = 'Marketing'
    OTHER = 'Other'

# Association table for user interests
user_interests = db.Table(
    'user_interests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True)
)


class Interest(db.Model):
    __tablename__ = 'interest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    users = db.relationship(
        'User',
        secondary=user_interests,
        back_populates='interests'
    )



# Models
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.String(250))
    role = db.Column(db.Enum(UserRole))
    certifications = db.Column(db.String(250))
    endorsements = db.Column(db.Integer, default=0)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    profile_image = db.Column(db.String(250))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    interests = db.relationship(
        'Interest',
        secondary=user_interests,
        back_populates='users'
    )
    job_applications = db.relationship('JobApplication', backref='user', lazy=True)
    media_files = db.relationship('UserMedia', back_populates='user')
    images = db.relationship('UserImage', back_populates='user')

    def serialize(self, include_interests=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'role': self.role.value if self.role else None,
            'certifications': self.certifications,
            'endorsements': self.endorsements,
            'city': self.city,
            'state': self.state,
            'profile_image': self.profile_image,
            'company': self.company.serialize() if self.company else None
        }
        if include_interests:
            data['interests'] = [interest.name for interest in self.interests]
        return data



class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    employees = db.relationship('User', backref='company', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description,
            'employees': [employee.id for employee in self.employees]
        }

class Connection(db.Model):
    __tablename__ = 'connection'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    connected_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String, default='pending')  # pending, connected, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', 
                          foreign_keys=[user_id],
                          backref=db.backref('initiated_connections', lazy=True))
    connected_user = db.relationship('User',
                                   foreign_keys=[connected_user_id],
                                   backref=db.backref('received_connections', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'connected_user_id': self.connected_user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class FavoriteConnect(db.Model):
    __tablename__ = 'favorite_connect'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', foreign_keys=[user_id], backref='favorite_connections')
    favorite_user = db.relationship('User', foreign_keys=[favorite_user_id], backref='favorited_by')

class JobPosting(db.Model):
    __tablename__ = 'job_posting'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=True)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('JobComment', backref='job_posting', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'salary': self.salary,
            'posted_by': self.posted_by,
            'created_at': self.created_at.isoformat(),
            'comments': [comment.serialize() for comment in self.comments]
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class JobComment(db.Model):
    __tablename__ = 'job_comment'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='job_comments')

    def serialize(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at.isoformat()
        }

class JobApplication(db.Model):
    __tablename__ = 'job_application'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, default='pending')  # pending, accepted, rejected

    job = db.relationship('JobPosting', backref='applications', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'applied_at': self.applied_at.isoformat(),
            'status': self.status
        }


class UserMedia(db.Model):
    __tablename__ = 'user_media'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # 'image' or 'video'
    file_path = db.Column(db.String(255), nullable=False)
    instructional = db.Column(db.Boolean, default=False)  # True for instructional videos
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='media_files')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'file_name': self.file_name,
            'file_type': self.file_type,
            'file_path': self.file_path,
            'instructional': self.instructional,
            'uploaded_at': self.uploaded_at.isoformat()
        }

class UserImage(db.Model):
    __tablename__ = 'user_images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='images')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'uploaded_at': self.uploaded_at.isoformat()
        }