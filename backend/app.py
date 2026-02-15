from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager  
from sqlalchemy import create_engine
from models import Base
from flask_cors import CORS
from sqlalchemy.orm import sessionmaker




app = Flask(__name__)
CORS(app)


engine= create_engine('sqlite:///campus_connect.db')
Base.metadata.create_all(engine)
sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)


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

# Resources (in resources/ folder or same file)
from resources.auth import Register, Login
from resources.company import CompanyRegistration, CompanyApprovalList, CompanyApprovalAction
from resources.student import StudentProfileResource
from resources.placement_drive import PlacementDriveResource, PlacementDriveList
from resources.admin import company_list, student_list, placement_stats



#Register all the routes
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')


api.add_resource(CompanyRegistration, '/company/register')
api.add_resource(CompanyApprovalList, '/company/approval-list')
api.add_resource(CompanyApprovalAction, '/company/approve/<int:company_id>')
api.add_resource(StudentProfileResource, '/student/profile')
api.add_resource(PlacementDriveResource, '/placement-drive/<int:drive_id>')
api.add_resource(PlacementDriveList, '/placement-drives')


api.add_resource(company_list, '/admin/companies')
api.add_resource(student_list, '/admin/students')
api.add_resource(placement_stats, '/admin/placement-stats')




if __name__ == '__main__':
    app.run(debug=True, port=5000)