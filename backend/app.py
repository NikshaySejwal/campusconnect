from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from models import Base, engine
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
CORS(app)

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
    StudentProfileResource, StudentDrivesResource, StudentApplyResource, StudentApplicationsResource
)



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

# Student routes
api.add_resource(StudentListResource, '/admin/students')
api.add_resource(StudentProfileResource, '/student/profile')
api.add_resource(StudentApplyResource, '/student/drive/<int:drive_id>/apply')
api.add_resource(StudentApplicationsResource, '/student/applications')

# Admin routes
api.add_resource(UserBlacklistResource, '/admin/user/<int:user_id>/blacklist')
api.add_resource(AdminStatsResource, '/admin/stats')
api.add_resource(AdminSearchResource, '/admin/search')




if __name__ == '__main__':
    app.run(debug=True, port=5000)