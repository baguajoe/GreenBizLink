from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db, User, Connection, FavoriteConnect, JobPosting, JobComment, JobApplication


api = Blueprint('api', __name__)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi'}
INSTRUCTIONAL_VIDEO_FOLDER = 'uploads/instructional_videos'

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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

@api.route('/job/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_job(job_id):
    user_id = get_jwt_identity()
    if 'resume' not in request.files:
        return jsonify({"error": "Resume file is required"}), 400

    resume = request.files['resume']
    filename = secure_filename(resume.filename)
    file_path = os.path.join("uploads/resumes", filename)
    resume.save(file_path)

    application = JobApplication(
        user_id=user_id,
        job_id=job_id,
        resume_file_path=file_path
    )
    db.session.add(application)
    db.session.commit()

    return jsonify(application.serialize()), 201


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


@api.route('/upload/video', methods=['POST'])
@jwt_required()
def upload_video():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Role-based restrictions
    if user.role not in [UserRole.CUSTOMER, UserRole.DISPENSARY_OWNER, UserRole.GROWER, UserRole.SEEDBANK_OWNER]:
        return jsonify({"error": "You do not have permission to upload videos"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        return jsonify({"error": "File type not allowed"}), 400

    # Determine the target folder
    if user.role in [UserRole.DISPENSARY_OWNER, UserRole.GROWER, UserRole.SEEDBANK_OWNER]:
        target_directory = INSTRUCTIONAL_VIDEO_FOLDER
    else:
        target_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'videos')

    os.makedirs(target_directory, exist_ok=True)

    # Save the file securely
    filename = secure_filename(file.filename)
    file_path = os.path.join(target_directory, filename)
    file.save(file_path)

    # Store video metadata in the database
    new_media = UserMedia(
        user_id=current_user_id,
        file_name=filename,
        file_type='video',
        file_path=file_path
    )
    db.session.add(new_media)
    db.session.commit()

    return jsonify(new_media.serialize()), 201

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
