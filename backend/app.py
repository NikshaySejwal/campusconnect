import os
from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import Base, engine, Users, UserRole, StudentProfile
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from celery_app import init_celery

# --- App Initialization ---
app = Flask(__name__)
CORS(app)
api = Api(app)

# --- App Configuration ---
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['UPLOAD_FOLDER'] = 'backend/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# --- Services Initialization ---
jwt = JWTManager(app)
celery_app = init_celery(app)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# --- Ensure upload directory exists ---
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# --- Database Initialization & Seeding ---
def init_db():
    Base.metadata.create_all(engine)
    # Seed admin user if it doesn't exist
    if not db.query(Users).filter(Users.role == UserRole.Admin).first():
        admin_user = Users(
            name='Admin',
            email="admin@mad2.com",
            password="admin123",
            role=UserRole.Admin,
        )
        db.add(admin_user)
        db.commit()

init_db()


# --- Helper Functions ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# --- Resources ---
from tasks import student_csv_export
from contollers import (
    RegisterResource, LoginResource, CompaniesList, CompanyStatusResource,
    DrivesListResource, DriveStatusResource, StudentListResource, UserBlacklistResource,
    AdminStatsResource, AdminSearchResource, CompanyProfileResource, CompanyDrivesResource,
    CompanyDriveApplicationsResource, CompanyApplicationStatusResource,
    StudentProfileResource, StudentDrivesResource, StudentApplyResource, StudentApplicationsResource,
    PublicDrivesResource, PublicDriveResource, AdminCompanyResource, AdminDriveResource,
    StudentProfileViewResource, StudentExportResource
)

class AvatarUploadResource(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        student_profile = db.query(StudentProfile).filter_by(user_id=user_id).first()

        if not student_profile:
            return {'message': 'Student profile not found'}, 404
        
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
            
        if file and allowed_file(file.filename):
            # Create a secure, unique filename
            filename = f"avatar_{user_id}_{secure_filename(file.filename)}"
            
            # Ensure the upload folder exists before saving
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                
            filepath = os.path.join(upload_folder, filename)
            
            # Delete old avatar if it exists
            if student_profile.avatar_url:
                try:
                    old_path = os.path.join(upload_folder, os.path.basename(student_profile.avatar_url))
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception as e:
                    print(f"Error deleting old avatar: {e}") # Log error

            file.save(filepath)
            
            # The URL should be relative to the server root
            avatar_url = f'/uploads/{filename}'
            student_profile.avatar_url = avatar_url
            db.commit()
            
            return {'message': 'Avatar updated successfully', 'avatar_url': avatar_url}, 200
        else:
            return {'message': 'File type not allowed'}, 400

class StudentExport(Resource):
    @jwt_required()
    def get(self, student_id):
        user_id = get_jwt_identity()
        if user_id != student_id:
            return {'error': 'Unauthorized'}, 403
        
        task = student_csv_export.delay(student_id)
        return {'task_id': task.id, 'status': 'processing'}, 202


# --- API Routes ---
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')

# Public Routes
api.add_resource(PublicDrivesResource, '/drives')
api.add_resource(PublicDriveResource, '/drive/<int:drive_id>')

# Student Routes
api.add_resource(StudentProfileResource, '/student/profile')
api.add_resource(StudentProfileViewResource, '/student/<int:student_id>/profile')
api.add_resource(StudentDrivesResource, '/student/drives')
api.add_resource(StudentApplyResource, '/student/drive/<int:drive_id>/apply')
api.add_resource(StudentApplicationsResource, '/student/applications')
api.add_resource(StudentExportResource, '/student/export')
api.add_resource(AvatarUploadResource, '/student/avatar') # New avatar upload route

# Company Routes
api.add_resource(CompanyProfileResource, '/company/profile')
api.add_resource(CompanyDrivesResource, '/company/drives')
api.add_resource(CompanyDriveApplicationsResource, '/company/drive/<int:drive_id>/applications')
api.add_resource(CompanyApplicationStatusResource, '/company/application/<int:application_id>/status')

# Admin Routes
api.add_resource(AdminStatsResource, '/admin/stats')
api.add_resource(AdminSearchResource, '/admin/search')
api.add_resource(CompaniesList, '/admin/companies')
api.add_resource(CompanyStatusResource, '/admin/company/<int:company_id>/status')
api.add_resource(DrivesListResource, '/admin/drives')
api.add_resource(DriveStatusResource, '/admin/drive/<int:drive_id>/status')
api.add_resource(StudentListResource, '/admin/students')
api.add_resource(UserBlacklistResource, '/admin/user/<int:user_id>/blacklist')
api.add_resource(AdminCompanyResource, '/admin/company/<int:company_id>')
api.add_resource(AdminDriveResource, '/admin/drive/<int:drive_id>')


# --- Static File Serving ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
