from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import Base, engine
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker
from celery_app import init_celery
from tasks import student_csv_export

app = Flask(__name__)
CORS(app)

# Add to app config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize
celery_app = init_celery(app)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#jwt config
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key in production
jwt = JWTManager(app)
api = Api(app)


#models
from models import Users, UserRole,CompanyApprovalStatus,DriveStatus, CompanyProfile, StudentProfile, PlacementDrive, Application, PlacementStat


# ensure an admin user exists
def seed_admin_user():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # use filter with expression (or filter_by with keyword)
        if not session.query(Users).filter(Users.role == UserRole.Admin).first():
            admin_user = Users(
                name='Admin',
                email="admin@mad2.com",
                password="admin123",
                role=UserRole.Admin,
            )
            session.add(admin_user)
            session.commit()
    finally:
        session.close()

# run seeding at startup
seed_admin_user()

# Resources from contollers.py
from contollers import (
    RegisterResource, LoginResource, CompaniesList, CompanyStatusResource,
    DrivesListResource, DriveStatusResource, StudentListResource, UserBlacklistResource,
    AdminStatsResource, AdminSearchResource, CompanyProfileResource, CompanyDrivesResource,
    CompanyDriveApplicationsResource, CompanyApplicationStatusResource,
    StudentProfileResource, StudentDrivesResource, StudentApplyResource, StudentApplicationsResource,
    PublicDrivesResource, PublicDriveResource
)

class StudentExport(Resource):
    @jwt_required()
    def get(self, student_id):
        user_id = get_jwt_identity()
        if user_id != student_id:
            return {'error': 'Unauthorized'}, 403
        
        task = student_csv_export.delay(student_id)
        return {'task_id': task.id, 'status': 'processing'}, 202

# Register all the routes
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')

# Company routes
api.add_resource(CompaniesList, '/admin/companies')
api.add_resource(CompanyStatusResource, '/admin/company/<int:company_id>/status')
api.add_resource(CompanyProfileResource, '/company/profile')
api.add_resource(CompanyDrivesResource, '/company/drives')
api.add_resource(CompanyDriveApplicationsResource, '/company/drive/<int:drive_id>/applications')
api.add_resource(CompanyApplicationStatusResource, '/company/application/<int:application_id>/status')

# Placement drive routes
api.add_resource(DrivesListResource, '/admin/drives')
api.add_resource(DriveStatusResource, '/admin/drive/<int:drive_id>/status')
api.add_resource(StudentDrivesResource, '/student/drives')
api.add_resource(PublicDrivesResource, '/drives')
api.add_resource(PublicDriveResource, '/drive/<int:drive_id>')

# Student routes
api.add_resource(StudentListResource, '/admin/students')
api.add_resource(StudentProfileResource, '/student/profile')
api.add_resource(StudentApplyResource, '/student/drive/<int:drive_id>/apply')
api.add_resource(StudentApplicationsResource, '/student/applications')
api.add_resource(StudentExport, '/api/student/export/<int:student_id>')

# Admin routes
api.add_resource(UserBlacklistResource, '/admin/user/<int:user_id>/blacklist')
api.add_resource(AdminStatsResource, '/admin/stats')
api.add_resource(AdminSearchResource, '/admin/search')

if __name__ == '__main__':
    app.run(debug=True, port=5000)