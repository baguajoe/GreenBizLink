from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.security import generate_password_hash
from api.models import db, User, Connection, FavoriteConnect, JobPosting, JobComment, JobApplication, TokenBlocklist, UserRole, Advertisement
from datetime import datetime

api = Blueprint('api', __name__)


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi'}
INSTRUCTIONAL_VIDEO_FOLDER = 'uploads/instructional_videos'

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@api.route('/signup', methods=['POST'])
def sign_up():
    try:
        data = request.json
        
        # Check if required data exists
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Get data from request
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        state = data.get("state")
        city = data.get("city")
        
        # Validate required fields
        if not email or not password or not full_name:
            return jsonify({"error": "Required fields missing (email, password, full_name)"}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400

        # Create new user
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password),
            name=full_name,
            state=state if state else None,
            city=city if city else None
        )
        
        # Add and commit to database
        db.session.add(new_user)
        db.session.commit()

        # Create response with just the basic user data
        response_body = {
            "message": "User successfully created",
            "user": new_user.serialize()  # Using basic serialization without relations
        }

        return jsonify(response_body), 201

    except Exception as e:
        # Roll back the session in case of error
        db.session.rollback()
        return jsonify({
            "error": "An error occurred while creating the user",
            "details": str(e)
        }), 500


@api.route('/login', methods=['POST'])
def login():
    try:
        # Get data from request body
        request_data = request.get_json()
        
        # Extract email and password from request
        email = request_data.get('email')
        password = request_data.get('password')
        
        # Validate required fields
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
            
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            # Create access token
            access_token = create_access_token(identity=user.id)
            return jsonify({
                "message": "Login successful",
                "access_token": access_token
            }), 200
        
        return jsonify({"error": "Invalid email or password"}), 401
        
    except Exception as e:
        print("Login error:", str(e))
        return jsonify({"error": "An error occurred during login"}), 500




# ----- FAVORITE CONNECTS ROUTES -----

@api.route('/favorite-connects/<int:user_id>/add', methods=['POST'])
def add_favorite_connect(user_id):
    data = request.json
    favorite_user_id = data.get('favorite_user_id')  # The ID of the user to be favorited

    if not favorite_user_id:
        return jsonify({'error': 'favorite_user_id is required'}), 400

    # Ensure both users exist
    user = User.query.get(user_id)
    favorite_user = User.query.get(favorite_user_id)

    if not user or not favorite_user:
        return jsonify({'error': 'User(s) not found'}), 404

    # Add favorite connection
    favorite_connect = FavoriteConnect(user_id=user_id, favorite_user_id=favorite_user_id)
    db.session.add(favorite_connect)
    db.session.commit()

    return jsonify({'message': 'Favorite connection added successfully'}), 201

@api.route('/favorite-connects/<int:favorite_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_favorite_connect(favorite_id):
    current_user_id = get_jwt_identity()
    favorite = FavoriteConnect.query.filter_by(id=favorite_id, user_id=current_user_id).first()

    if not favorite:
        return jsonify({"error": "Favorite connect not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite connect removed successfully"}), 200

# ----- CONNECTIONS ROUTES -----

@api.route('/connections/<int:user_id>/add', methods=['POST'])
@jwt_required()
def add_connection(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return jsonify({"error": "Cannot connect with yourself"}), 400

    existing_connection = Connection.query.filter_by(user_id=current_user_id, connected_user_id=user_id).first()
    if existing_connection:
        return jsonify({"error": "Connection already exists"}), 400

    new_connection = Connection(user_id=current_user_id, connected_user_id=user_id, status="pending")
    db.session.add(new_connection)
    db.session.commit()

    return jsonify({"message": "Connection request sent"}), 201

@api.route('/connections/<int:connection_id>/delete', methods=['DELETE'])
@jwt_required()
def delete_connection(connection_id):
    current_user_id = get_jwt_identity()
    connection = Connection.query.filter_by(id=connection_id, user_id=current_user_id).first()

    if not connection:
        return jsonify({"error": "Connection not found"}), 404

    db.session.delete(connection)
    db.session.commit()

    return jsonify({"message": "Connection deleted successfully"}), 200

# ----- JOB POSTINGS ROUTES -----

@api.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = JobPosting.query.all()
    return jsonify([job.serialize() for job in jobs]), 200

@api.route('/job', methods=['POST'])
@jwt_required()
def create_job():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    salary = data.get('salary')
    user_id = get_jwt_identity()

    if not title or not description or not location:
        return jsonify({"error": "Title, description, and location are required"}), 400

    new_job = JobPosting(title=title, description=description, location=location, salary=salary, posted_by=user_id)
    db.session.add(new_job)
    db.session.commit()

    return jsonify(new_job.serialize()), 201

@api.route('/job/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    user_id = get_jwt_identity()
    job = JobPosting.query.get(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404
    if job.posted_by != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(job)
    db.session.commit()

    return jsonify({"message": "Job deleted successfully"}), 200

# ----- COMMENTS ROUTES -----

@api.route('/job/<int:job_id>/comments', methods=['GET'])
def get_job_comments(job_id):
    job = JobPosting.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify([comment.serialize() for comment in job.comments]), 200

@api.route('/job/<int:job_id>/comment', methods=['POST'])
@jwt_required()
def add_job_comment(job_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')
    parent_id = data.get('parent_id')  # Allow nested comments

    if not content:
        return jsonify({"error": "Content is required"}), 400

    new_comment = JobComment(
        job_id=job_id,
        user_id=user_id,
        content=content,
        parent_id=parent_id
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.serialize()), 201


# ----- JOB APPLICATIONS ROUTES -----

# @api.route('/job/<int:job_id>/apply', methods=['POST'])
# @jwt_required()
# def apply_for_job(job_id):
#     user_id = get_jwt_identity()
#     if 'resume' not in request.files:
#         return jsonify({"error": "Resume file is required"}), 400

#     resume = request.files['resume']
#     filename = secure_filename(resume.filename)
#     file_path = os.path.join("uploads/resumes", filename)
#     resume.save(file_path)

#     application = JobApplication(
#         user_id=user_id,
#         job_id=job_id,
#         resume_file_path=file_path
#     )
#     db.session.add(application)
#     db.session.commit()

#     return jsonify(application.serialize()), 201


@api.route('/job/<int:job_id>/applications/<int:application_id>/status', methods=['PATCH'])
@jwt_required()
def update_application_status(job_id, application_id):
    user = get_jwt_identity()
    application = JobApplication.query.get(application_id)

    if not application or application.job_id != job_id:
        return jsonify({"error": "Application not found"}), 404

    # Ensure only hiring managers can review applications
    job = JobPosting.query.get(job_id)
    if job.company_id != user['company_id']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    new_status = data.get("status")
    decision_notes = data.get("decision_notes", "")

    if new_status not in ["pending", "accepted", "rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    application.status = new_status
    application.decision_notes = decision_notes
    db.session.commit()

    return jsonify({"message": "Application status updated"}), 200


# @api.route('/upload/video', methods=['POST'])
# @jwt_required()
# def upload_video():
#     current_user_id = get_jwt_identity()
#     user = User.query.get(current_user_id)

#     # Role-based restrictions
#     if user.role not in [UserRole.CUSTOMER, UserRole.DISPENSARY_OWNER, UserRole.GROWER, UserRole.SEEDBANK_OWNER]:
#         return jsonify({"error": "You do not have permission to upload videos"}), 403

#     if 'file' not in request.files:
#         return jsonify({"error": "No file part in the request"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
#         return jsonify({"error": "File type not allowed"}), 400

#     # Determine the target folder
#     if user.role in [UserRole.DISPENSARY_OWNER, UserRole.GROWER, UserRole.SEEDBANK_OWNER]:
#         target_directory = INSTRUCTIONAL_VIDEO_FOLDER
#     else:
#         target_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos')

#     os.makedirs(target_directory, exist_ok=True)

#     # Save the file securely
#     filename = secure_filename(file.filename)
#     file_path = os.path.join(target_directory, filename)
#     file.save(file_path)

#     # Store video metadata in the database
#     new_media = UserMedia(
#         user_id=current_user_id,
#         file_name=filename,
#         file_type='video',
#         file_path=file_path
#     )
#     db.session.add(new_media)
#     db.session.commit()

#     return jsonify(new_media.serialize()), 201

@api.route('/stream/video/<filename>', methods=['GET'])
@jwt_required()
def stream_video(filename):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Check if it’s an instructional video and verify access
    instructional_video_path = os.path.join(INSTRUCTIONAL_VIDEO_FOLDER, filename)
    if os.path.exists(instructional_video_path):
        if user.role not in [UserRole.DISPENSARY_OWNER, UserRole.GROWER, UserRole.SEEDBANK_OWNER]:
            return jsonify({"error": "You do not have access to instructional videos"}), 403
        video_path = instructional_video_path
    else:
        video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos', filename)

    # Check if video exists
    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404

    return partial_response(video_path)


@api.route('/images/<filename>', methods=['GET'])
@jwt_required()
def get_image(filename):
    image_path = os.path.join(IMAGE_UPLOAD_FOLDER, filename)

    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    return send_file(image_path)


@api.route('/companies/<int:company_id>/jobs', methods=['POST'])
@jwt_required()
def post_job(company_id):
    user = get_jwt_identity()
    company = Company.query.get(company_id)

    if not company:
        return jsonify({"error": "Company not found"}), 404

    user_obj = User.query.get(user['id'])

    # Ensure user is part of the company and has permission
    if user_obj.company_id != company_id or user_obj.role not in ["DISPENSARY_OWNER", "GROWER", "MANAGER"]:
        return jsonify({"error": "Unauthorized to post jobs"}), 403

    # Extract job details
    data = request.get_json()
    title = data.get("title")
    category = data.get("category")
    description = data.get("description")
    location = data.get("location")
    salary = data.get("salary")

    if not title or not description or not location:
        return jsonify({"error": "Title, description, and location are required"}), 400

    # Create new job posting
    new_job = JobPosting(
        title=title,
        category=category,
        description=description,
        location=location,
        salary=salary,
        posted_by=user['id'],
        company_id=company_id
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job posted successfully", "job": new_job.serialize()}), 201  

@api.route('/companies/<int:company_id>/jobs', methods=['GET'])
def get_company_jobs(company_id):
    jobs = JobPosting.query.filter_by(company_id=company_id).all()
    return jsonify([job.serialize() for job in jobs])


# authentification

# @api.route("/register", methods=["POST"])
# def register():
#     data = request.get_json()
#     name = data.get("name")
#     email = data.get("email")
#     password = data.get("password")
#     city = data.get("city")
#     state = data.get("state")
#     role = data.get("role")  # Role must match UserRole Enum values
#     company_name = data.get("company_name")  # Optional for business owners
#     company_industry = data.get("company_industry")  # Optional for business owners

#     # Validate required fields
#     if not all([name, email, password, city, state, role]):
#         return jsonify({"error": "Missing required fields"}), 400

#     # Ensure the role is valid
#     try:
#         user_role = UserRole(role)  # Convert string to Enum
#     except ValueError:
#         return jsonify({"error": "Invalid role"}), 400

#     # Check if email is already registered
#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return jsonify({"error": "User already exists"}), 400

#     # Hash the password
#     hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

#     # Create new user
#     new_user = User(
#         name=name,
#         email=email,
#         password_hash=hashed_password,
#         city=city,
#         state=state,
#         role=user_role
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     # If the user is a Business Owner, create a company
#     if role in ["Dispensary Owner", "Grower"] and company_name:
#         new_company = Company(
#             name=company_name,
#             industry=company_industry,
#             company_size="Small",  # Default size
#             location=f"{city}, {state}",
#             verified=False,
#             email=email
#         )
#         db.session.add(new_company)
#         db.session.commit()

#         new_user.company_id = new_company.id
#         db.session.commit()

#     # Generate email verification token
#     verification_token = jwt.encode(
#         {"email": new_user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
#         app.config["JWT_SECRET_KEY"],
#         algorithm="HS256"
#     )

#     verification_url = url_for("verify_email", token=verification_token, _external=True)
#     send_verification_email(email, verification_url)

#     # Auto-login user
#     access_token = create_access_token(identity={"id": new_user.id, "email": new_user.email})

#     return jsonify({
#         "message": "User registered successfully. Please check your email to verify your account.",
#         "user": {
#             "id": new_user.id,
#             "name": new_user.name,
#             "email": new_user.email,
#             "city": new_user.city,
#             "state": new_user.state,
#             "role": new_user.role.value
#         },
#         "access_token": access_token
#     }), 201


# @api.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     # Check if user exists
#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({"error": "Invalid email or password"}), 401

#     # Verify password
#     if not bcrypt.check_password_hash(user.password_hash, password):
#         return jsonify({"error": "Invalid email or password"}), 401

#     # Ensure the user has verified their email
#     if not user.is_verified:
#         return jsonify({"error": "Please verify your email before logging in."}), 403

#     # Generate JWT Access & Refresh Tokens
#     access_token = create_access_token(identity={
#         "id": user.id,
#         "email": user.email,
#         "role": user.role.value,  # Include role for RBAC
#         "city": user.city,
#         "state": user.state
#     })
#     refresh_token = create_refresh_token(identity={"id": user.id, "email": user.email})

#     # Log last login time
#     user.last_login = datetime.utcnow()
#     db.session.commit()

#     return jsonify({
#         "message": "Login successful",
#         "access_token": access_token,
#         "refresh_token": refresh_token,  # Allows user to refresh session
#         "user": {
#             "id": user.id,
#             "name": user.name,
#             "email": user.email,
#             "role": user.role.value,
#             "city": user.city,
#             "state": user.state,
#             "last_login": user.last_login.isoformat()
#         }
#     }), 200

@api.route("/logout", methods=["POST"])
@jwt_required(refresh=True)  # Requires refresh token to log out
def logout():
    jti = get_jwt()["jti"]  # Get JWT Token ID
    db.session.add(TokenBlocklist(jti=jti))  # Add to blocklist
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200

@api.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    try:
        decoded_data = jwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        user_email = decoded_data["email"]
        user = User.query.filter_by(email=user_email).first()

        if not user:
            return jsonify({"error": "Invalid token"}), 400

        # Mark user as verified (optional: add `is_verified` column to the User model)
        user.is_verified = True
        db.session.commit()

        return jsonify({"message": "Email verified successfully. You can now log in."}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Verification link expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid verification link"}), 400


@api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token}), 200


@api.route("/users/pending_requests", methods=["GET"])
@jwt_required()
def get_pending_requests():
    """Fetch all connection requests received by the user that are pending."""
    current_user_id = get_jwt_identity()["id"]

    pending_requests = Connection.query.filter_by(connected_user_id=current_user_id, status="pending").all()

    return jsonify([{
        "id": conn.id,
        "user_id": conn.user_id,
        "user_name": conn.user.name,
        "user_role": conn.user.role.value,
        "user_city": conn.user.city,
        "user_state": conn.user.state
    } for conn in pending_requests]), 200


@api.route("/users/connection/<int:connection_id>", methods=["PATCH"])
@jwt_required()
def update_connection_status(connection_id):
    """Accept or reject a connection request."""
    data = request.get_json()
    new_status = data.get("status")  # Accept or reject
    if new_status not in ["connected", "rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    connection = Connection.query.get(connection_id)
    if not connection:
        return jsonify({"error": "Connection request not found"}), 404

    connection.status = new_status
    db.session.commit()

    return jsonify({"message": f"Connection request {new_status}."}), 200


@api.route("/users/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    """Fetch notifications for connection requests."""
    current_user_id = get_jwt_identity()["id"]

    notifications = Connection.query.filter_by(connected_user_id=current_user_id, status="pending").all()

    return jsonify([{
        "message": f"{conn.user.name} sent you a connection request.",
        "timestamp": conn.created_at.isoformat()
    } for conn in notifications]), 200


@api.route("/users/favorites", methods=["GET"])
@jwt_required()
def get_favorite_users():
    """Fetch all favorited users."""
    current_user_id = get_jwt_identity()["id"]

    favorites = FavoriteConnect.query.filter_by(user_id=current_user_id).all()

    return jsonify([{
        "id": fav.favorite_user.id,
        "name": fav.favorite_user.name,
        "role": fav.favorite_user.role.value,
        "city": fav.favorite_user.city,
        "state": fav.favorite_user.state
    } for fav in favorites]), 200


# advertising

@api.route("/ads", methods=["GET"])
def get_ads():
    """Fetch all active advertisements."""
    ads = Advertisement.query.filter_by(active=True).all()
    return jsonify([ad.serialize() for ad in ads]), 200


@api.route("/ads", methods=["POST"])
@jwt_required()
def create_ad():
    """Allow companies to create advertisements."""
    current_user_id = get_jwt_identity()["id"]
    user = User.query.get(current_user_id)

    if not user or not user.company_id:
        return jsonify({"error": "Only companies can create ads"}), 403

    data = request.get_json()
    new_ad = Advertisement(
        company_id=user.company_id,
        title=data.get("title"),
        description=data.get("description"),
        image_url=data.get("image_url"),
        link=data.get("link")
    )
    db.session.add(new_ad)
    db.session.commit()

    return jsonify(new_ad.serialize()), 201


@api.route("/ads/<int:ad_id>/toggle", methods=["PATCH"])
@jwt_required()
def toggle_ad_status(ad_id):
    """Allow an admin to activate/deactivate an ad."""
    current_user_id = get_jwt_identity()["id"]
    user = User.query.get(current_user_id)

    if not user or user.role != UserRole.ADMIN:
        return jsonify({"error": "Unauthorized"}), 403

    ad = Advertisement.query.get(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404

    ad.active = not ad.active  # Toggle status
    db.session.commit()

    return jsonify({"message": f"Ad {'activated' if ad.active else 'deactivated'}"}), 200
