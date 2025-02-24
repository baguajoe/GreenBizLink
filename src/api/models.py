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
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    bio = db.Column(db.String(250))
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)  # Default to 'Customer'
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    profile_image = db.Column(db.String(250))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    # New Fields
    is_verified = db.Column(db.Boolean, default=False)  # Tracks email verification
    last_login = db.Column(db.DateTime, nullable=True)  # Tracks last login time

    # Relationships
    interests = db.relationship("Interest", secondary=user_interests, back_populates="users")
    job_applications = db.relationship("JobApplication", back_populates="user", lazy=True)
    media_files = db.relationship("UserMedia", back_populates="user")
    images = db.relationship("UserImage", back_populates="user")

    def serialize(self, include_interests=False):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "bio": self.bio,
            "role": self.role.value if self.role else None,
            "city": self.city,
            "state": self.state,
            "profile_image": self.profile_image,
            "company": self.company.serialize() if self.company else None,
            "is_verified": self.is_verified,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
        if include_interests:
            data["interests"] = [interest.name for interest in self.interests]
        return data

class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)  # JWT Token ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {"id": self.id, "jti": self.jti, "created_at": self.created_at.isoformat()}


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)  # JWT Token ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = {'extend_existing': True}  # Fix duplicate definition issue

    def serialize(self):
        return {"id": self.id, "jti": self.jti, "created_at": self.created_at.isoformat()}


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    industry = db.Column(db.String(100))  # Grower, Dispensary, etc.
    company_size = db.Column(db.String(50))  # Small, Medium, Large
    location = db.Column(db.String(100))
    website = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    social_links = db.Column(db.String(255))  # {"linkedin": "...", "instagram": "..."}
    founded_year = db.Column(db.Integer)
    verified = db.Column(db.Boolean, default=False)  # Company verification status
    logo = db.Column(db.String(255))  # Company logo URL or file path
    description = db.Column(db.Text)

    # Relationships
    employees = db.relationship('User', backref='company', lazy=True, cascade="all, delete")
    jobs = db.relationship('JobPosting', back_populates='company', lazy=True, cascade="all, delete")
    videos = db.relationship('UserMedia', back_populates='company', lazy=True, cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "company_size": self.company_size,
            "location": self.location,
            "website": self.website,
            "phone": self.phone,
            "email": self.email,
            "social_links": self.social_links,
            "founded_year": self.founded_year,
            "verified": self.verified,
            "logo": self.logo,
            "description": self.description,
            "employees": [employee.id for employee in self.employees],
            "jobs": [job.id for job in self.jobs],
            "videos": [video.id for video in self.videos],
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
    category = db.Column(db.String(100), nullable=False)  # Budtender, Grower, etc.
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50))
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # Links job to company
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    company = db.relationship('Company', back_populates='jobs')

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "location": self.location,
            "salary": self.salary,
            "posted_by": self.posted_by,
            "company_id": self.company_id,
            "created_at": self.created_at.isoformat()
        }


class JobComment(db.Model):
    __tablename__ = 'job_comment'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # Links comment to a company
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('job_comment.id'))  # For threaded replies

    user = db.relationship('User', backref='job_comments')
    job = db.relationship('JobPosting', backref='comments', lazy=True)
    company = db.relationship('Company', backref='job_comments', lazy=True)
    parent_comment = db.relationship('JobComment', remote_side=[id], backref='replies')

    def serialize(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "user_id": self.user_id,
            "company_id": self.company_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "parent_id": self.parent_id,
            "replies": [reply.serialize() for reply in self.replies]
        }


class JobApplication(db.Model):
    __tablename__ = 'job_application'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job_posting.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # Links job application to company
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, default='pending')  # pending, accepted, rejected
    resume_file_path = db.Column(db.String(255))  # Stores file path of resume
    decision_notes = db.Column(db.Text)  # Private notes for hiring managers

    user = db.relationship('User', back_populates='job_applications', lazy=True)
    job = db.relationship('JobPosting', backref='applications', lazy=True)
    company = db.relationship('Company', backref='applications', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "company_id": self.company_id,
            "applied_at": self.applied_at.isoformat(),
            "status": self.status,
            "resume_file_path": self.resume_file_path,
            "decision_notes": self.decision_notes if self.status != "pending" else None
        }

class UserMedia(db.Model):
    __tablename__ = 'user_media'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # 'image' or 'video'
    file_path = db.Column(db.String(255), nullable=False)
    instructional = db.Column(db.Boolean, default=False)  # True for instructional videos
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='media_files')
    company = db.relationship('Company', back_populates='videos')

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
    

# advertising

class Advertisement(db.Model):
    __tablename__ = "advertisements"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))  # Optional image for the ad
    link = db.Column(db.String(255), nullable=False)  # External link for the ad
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    company = db.relationship("Company", backref="advertisements")

    def serialize(self):
        return {
            "id": self.id,
            "company": self.company.name,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "link": self.link,
            "created_at": self.created_at.isoformat(),
            "active": self.active
        }
